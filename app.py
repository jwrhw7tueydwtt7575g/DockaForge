import os
import re
import shutil
import subprocess
import requests
from utils.zip_handler import extract_zip
from utils.analyzer import detect_language
from utils.docker_ops import create_dockerfile, build_image

def docker_login(username, password):
    print("Attempting Docker login...")
    try:
        subprocess.run(
            ["docker", "login", "-u", username, "--password-stdin"],
            input=password.encode(), check=True
        )
        print("Docker login successful")
    except subprocess.CalledProcessError as e:
        print("Docker login failed:", e)
        raise Exception("Docker login failed. Check credentials.")

def generate_requirements(project_path, lang):
    """
    Auto-generate dependency files for supported languages:
    - Python: requirements.txt (pipreqs → pip freeze fallback)
    - NodeJS: package.json (scan imports)
    - Java: pom.xml (minimal placeholder)
    - Golang: go.mod (go mod init)
    - PHP: composer.json (scan `use` statements)
    - Ruby: Gemfile (scan `require` statements)
    """
    # PYTHON
    if lang == "python":
        req = os.path.join(project_path, "requirements.txt")
        if os.path.exists(req):
            return True
        try:
            subprocess.run(["pip", "install", "pipreqs"], check=True)
            subprocess.run(["pipreqs", project_path, "--force"], check=True)
            if os.path.getsize(req) > 0:
                print("requirements.txt generated via pipreqs.")
                return True
        except Exception:
            pass
        # fallback to pip freeze
        with open(req, "w") as f:
            f.write(subprocess.check_output(["pip", "freeze"], text=True))
        print("requirements.txt generated via pip freeze.")
        return True

    # NODEJS
    if lang == "nodejs":
        pkg = os.path.join(project_path, "package.json")
        if os.path.exists(pkg):
            return True
        deps = set()
        for ext in (".js", ".ts"):
            for root, _, files in os.walk(project_path):
                for fn in files:
                    if fn.endswith(ext):
                        text = open(os.path.join(root, fn), "r", errors="ignore").read()
                        for m in re.findall(r"""(?:require\(['"]([^'"]+)['"]\))|(?:from ['"]([^'"]+)['"] )""", text):
                            module = m[0] or m[1]
                            if not module.startswith((".", "/")):
                                deps.add(module.split("/")[0])
        pkgdata = {
            "name": "auto-app",
            "version": "1.0.0",
            "dependencies": {d: "*" for d in sorted(deps)}
        }
        import json
        with open(pkg, "w") as f:
            json.dump(pkgdata, f, indent=2)
        print("package.json created with detected dependencies.")
        return True

    # JAVA
    if lang == "java":
        pom = os.path.join(project_path, "pom.xml")
        if os.path.exists(pom):
            return True
        with open(pom, "w") as f:
            f.write(
                "<project xmlns=\"http://maven.apache.org/POM/4.0.0\">\n"
                "  <modelVersion>4.0.0</modelVersion>\n"
                "  <groupId>auto</groupId>\n"
                "  <artifactId>app</artifactId>\n"
                "  <version>1.0</version>\n"
                "</project>\n"
            )
        print("pom.xml placeholder created.")
        return True

    # GOLANG
    if lang == "golang":
        mod = os.path.join(project_path, "go.mod")
        if os.path.exists(mod):
            return True
        module = os.path.basename(project_path)
        subprocess.run(["go", "mod", "init", module], cwd=project_path, check=True)
        print("go.mod initialized.")
        return True

    # PHP
    if lang == "php":
        comp = os.path.join(project_path, "composer.json")
        if os.path.exists(comp):
            return True
        deps = {}
        for root, _, files in os.walk(project_path):
            for fn in files:
                if fn.endswith(".php"):
                    text = open(os.path.join(root, fn), "r", errors="ignore").read()
                    for m in re.findall(r"use\s+([^;]+);", text):
                        pkg = m.split("\\\\")[0]
                        deps[pkg.lower()] = "*"
        data = {"require": deps}
        import json
        with open(comp, "w") as f:
            json.dump(data, f, indent=2)
        print("composer.json created with detected packages.")
        return True

    # RUBY
    if lang == "ruby":
        gem = os.path.join(project_path, "Gemfile")
        if os.path.exists(gem):
            return True
        requires = set()
        for root, _, files in os.walk(project_path):
            for fn in files:
                if fn.endswith(".rb"):
                    text = open(os.path.join(root, fn), "r", errors="ignore").read()
                    for m in re.findall(r"require ['\"]([^'\"]+)['\"]", text):
                        if not m.startswith("."):
                            requires.add(m)
        with open(gem, "w") as f:
            f.write("source 'https://rubygems.org'\n")
            for r in sorted(requires):
                f.write(f"gem '{r}'\n")
        print("Gemfile created with detected gems.")
        return True

    return False

def flatten_project_dir(project_path):
    print("Flattening directory structure...")
    for root, _, files in os.walk(project_path):
        for file in files:
            if root != project_path and file != ".DS_Store":
                shutil.copy(
                    os.path.join(root, file),
                    os.path.join(project_path, file)
                )
    print("All files moved to project root.")

def push_to_github_repo(project_path, repo_name, github_username, github_token):
    print("Pushing project to GitHub...")
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.post(
        "https://api.github.com/user/repos",
        headers=headers,
        json={"name": repo_name, "private": False}
    )
    if response.status_code not in (201, 422):
        print("GitHub repo creation failed:", response.json())
        return "GitHub repo creation failed."
    print("GitHub repo ready.")

    try:
        subprocess.run(["git", "init"], cwd=project_path, check=True)
        subprocess.run(["git", "config", "user.email", f"{github_username}@users.noreply.github.com"], cwd=project_path, check=True)
        subprocess.run(["git", "config", "user.name", github_username], cwd=project_path, check=True)
        subprocess.run(["git", "add", "."], cwd=project_path, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=project_path, check=True)
        subprocess.run(["git", "branch", "-M", "main"], cwd=project_path, check=True)
        remote = f"https://{github_username}:{github_token}@github.com/{github_username}/{repo_name}.git"
        subprocess.run(["git", "remote", "add", "origin", remote], cwd=project_path, check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=project_path, check=True)
        print("Code pushed to GitHub.")
        return f"https://github.com/{github_username}/{repo_name}"
    except subprocess.CalledProcessError as e:
        return f"Git push failed: {e}"

def deploy(zip_path, docker_username, docker_password, github_username, github_token):
    project_path = extract_zip(zip_path)
    print("Project extracted to:", project_path)

    lang = detect_language(project_path)
    print("Detected language:", lang)
    if lang == "unknown":
        return "Unsupported project type"

    # Generate dependencies
    if not generate_requirements(project_path, lang):
        return f"Could not generate dependencies for {lang}"

    flatten_project_dir(project_path)

    create_dockerfile(project_path, lang)
    print("Dockerfile created")

    try:
        docker_login(docker_username, docker_password)
    except Exception as e:
        return str(e)

    image_tag = f"{docker_username}/{os.path.basename(project_path)}"
    try:
        build_image(project_path, image_tag)
        print("Docker image built:", image_tag)
    except subprocess.CalledProcessError:
        return "Docker build failed. Check Dockerfile."

    repo_url = push_to_github_repo(
        project_path, os.path.basename(project_path),
        github_username, github_token
    )

    return (
        f"Deployment complete!\n"
        f"Docker Image: {image_tag}\n"
        f"GitHub Repo: {repo_url}"
    )
