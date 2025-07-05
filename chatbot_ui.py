import os
import gradio as gr
from app import deploy

with gr.Blocks(css="""
    .gradio-container {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f5f5f5;
    }
    .gr-block {
        background: white;
        border-radius: 10px;
        padding: 30px;
        max-width: 700px;
        margin: 30px auto;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.08);
    }
    .gr-button {
        background-color: #007BFF !important;
        color: white !important;
        border-radius: 5px !important;
        padding: 10px 20px !important;
    }
    .gr-button:hover {
        background-color: #0056b3 !important;
    }
""") as demo:
    gr.Markdown("<h2 style='text-align:center;'>Docker + GitHub Auto Deployment</h2>")

    with gr.Row():
        file_input = gr.File(label="Upload Zipped Project (.zip)", file_types=[".zip"])

    with gr.Row():
        docker_user = gr.Textbox(label="DockerHub Username")
        docker_pass = gr.Textbox(label="DockerHub Password", type="password")

    with gr.Row():
        github_user = gr.Textbox(label="GitHub Username")
        github_token = gr.Textbox(label="GitHub Token (PAT)", type="password")

    deploy_btn = gr.Button("Deploy Now")
    output = gr.Textbox(label="Deployment Logs", lines=12, interactive=False)

    def handle_deploy(file, d_user, d_pass, g_user, g_token):
        if not file:
            return "❌ Please upload a .zip file."
        file_path = file.name
        return deploy(file_path, d_user, d_pass, g_user, g_token)

    deploy_btn.click(
        fn=handle_deploy,
        inputs=[file_input, docker_user, docker_pass, github_user, github_token],
        outputs=output
    )

demo.launch()
