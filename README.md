# 🚀 DockaForge

**DockaForge** is an automated deployment tool that allows users to:

- Upload a zipped project (Python Flask/FastAPI/Django or Node.js, etc.)
- Auto-detect the project type
- Auto-generate `requirements.txt` or `package.json`
- Auto-generate a `Dockerfile`
- Auto-build a Docker image
- Push the Docker image to Docker Hub
- Push the source code to a newly created GitHub repository (via PAT)

All with just **one click** via a web interface.

---

## 🖥️ Features

- ✅ Auto-detects project language (Python, Node.js)
- ✅ Auto-generates dependency files (`requirements.txt`, `package.json`)
- ✅ Dockerfile is automatically created based on language
- ✅ Builds and tags Docker image
- ✅ Pushes image to Docker Hub (via Docker CLI)
- ✅ Pushes code to GitHub (via GitHub REST API)
- ✅ Simple UI built with **Gradio**
- ✅ Optional: Flask version available as well

---

## 📁 Folder Structure

DockaForge/
│
├── app.py # Core backend logic for detection, docker build, GitHub push
├── chatbot_ui.py # Gradio-based frontend
├── utils/
│ ├── analyzer.py # Language detection utility
│ └── zip_handler.py # File extraction logic
├── docker_ops.py # Dockerfile generation & Docker CLI commands
├── temp_projects/ # Temporary uploads storage
└── README.md # You're reading it!

yaml
Copy
Edit

---

## 🌐 Live Demo

> https://youtu.be/8O3bSxBgarg

---

## 🧰 Requirements

- Python 3.8+
- Docker installed & running
- Git installed
- Internet connection (for GitHub API + Docker login)
- GitHub Personal Access Token (PAT) with `repo` scope
- DockerHub account

---

## 🚦 How to Use (Locally)

1. **Clone this repo**  
   ```bash
   git clone https://github.com/your-username/DockaForge.git
   cd DockaForge
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the app

bash
Copy
Edit
python chatbot_ui.py
Visit
Go to http://127.0.0.1:7860 in your browser.

Upload your zipped project and fill credentials:

DockerHub username and password

GitHub username and Personal Access Token (PAT)

📦 Supported Project Types
Language	Frameworks Supported
Python	Flask, FastAPI, Django, hybrid
JavaScript	Node.js, Express, Vite

More languages (e.g., Go, Java) coming soon.

🔐 GitHub Token Permission (PAT)
Ensure your token has the following scope:

nginx
Copy
Edit
repo
Generate one from here:
👉 https://github.com/settings/tokens

