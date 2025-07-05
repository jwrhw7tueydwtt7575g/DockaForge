from pyngrok import ngrok, conf

def expose_port(port):
    print(f"🌐 Trying to start ngrok tunnel on port {port}...")

    # (Optional) Set your ngrok authtoken here if not set globally
    # conf.get_default().auth_token = "your-ngrok-authtoken"

    try:
        public_url = ngrok.connect(port, "http").public_url
        print(f"✅ ngrok tunnel established at: {public_url}")
        return public_url
    except Exception as e:
        print("❌ ngrok tunnel failed:", str(e))
        raise Exception("Ngrok failed to start. Check your internet connection, ngrok config, or port usage.")

