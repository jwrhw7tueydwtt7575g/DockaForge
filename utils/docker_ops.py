import os
import subprocess
from shutil import copyfile

def create_dockerfile(project_path, lang):
    template_file = f"templates/{lang}.txt"
    dockerfile_path = os.path.join(project_path, "Dockerfile")
    copyfile(template_file, dockerfile_path)
    return dockerfile_path

def build_image(project_path, image_tag):
    subprocess.run(["docker", "build", "-t", image_tag, project_path], check=True)

def run_container(image_tag, port):
    subprocess.run(["docker", "run", "-d", "-p", f"{port}:{port}", image_tag], check=True)
