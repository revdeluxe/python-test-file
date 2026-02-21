import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from providers.google_llm import GoogleProvider
from providers.local_llm import LocalProvider

load_dotenv()
app = Flask(__name__)

# --- CONFIGURATION SWITCH ---
# Set this to "local" or "google"
USE_PROVIDER = "google" 

if USE_PROVIDER == "google":
    ai = GoogleProvider()
else:
    ai = LocalProvider(model_path="./models/gemma-3")
# ----------------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    try:
        response_text = ai.generate(user_input)
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    # Running on 0.0.0.0 allows your phone to access the server on your local network
    cert_path = 'static/certs/cert.pem'
    key_path = 'static/certs/key.pem'
    
    # Check if files exist to avoid silent errors
    if os.path.exists(cert_path) and os.path.exists(key_path):
        context = (cert_path, key_path)
        app.run(host='0.0.0.0', port=5000, ssl_context=context, debug=True)
    else:
        print("Certificates not found! Please check the static/certs/ folder.")