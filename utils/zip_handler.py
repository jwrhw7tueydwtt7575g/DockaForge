import zipfile
import os
import shutil
import uuid

def extract_zip(zip_path):
    project_id = f"project_{uuid.uuid4().hex[:8]}"
    extract_to = os.path.join("temp_projects", project_id)
    os.makedirs(extract_to, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return extract_to
