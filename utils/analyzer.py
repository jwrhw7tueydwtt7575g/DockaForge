import os

def detect_language(project_path):
    for root, _, files in os.walk(project_path):
        files_lower = [f.lower() for f in files]
        if "requirements.txt" in files_lower or any(f.endswith(".py") for f in files_lower):
            return "python"
        if "package.json" in files_lower or any(f.endswith(".js") or f.endswith(".ts") for f in files_lower):
            return "nodejs"
        if "pom.xml" in files_lower or any(f.endswith(".java") for f in files_lower):
            return "java"
        if "go.mod" in files_lower or any(f.endswith(".go") for f in files_lower):
            return "golang"
        if any(f.endswith(".php") for f in files_lower):
            return "php"
        if any(f.endswith(".rb") for f in files_lower):
            return "ruby"
    return "unknown"
