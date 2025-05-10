from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import logging

# ✅ Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

app = Flask(__name__)

# ✅ HIGHLIGHTED CHANGE — CORS now restricted to your GitHub Pages frontend
CORS(app, origins=["https://umesh-khm.github.io"], methods=["GET", "POST", "OPTIONS"])

# Hugging Face API endpoint
API_URL = "https://api-inference.huggingface.co/models/Salesforce/codegen-350M-multi"

# API Key from environment variable
HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    logging.error("Missing Hugging Face API key. Set HF_API_KEY in environment variables.")
    raise RuntimeError("HF_API_KEY not set.")

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

@app.route('/')
def home():
    return "✅ CodeGen API is up and running."

@app.route('/analyze', methods=['POST'])
def analyze_code():
    try:
        data = request.get_json()
        if not data:
            logging.warning("Request received without JSON body.")
            return jsonify({"error": "Missing JSON body"}), 400

        prompt = data.get("prompt")
        if not prompt:
            logging.warning("Request received without 'prompt'.")
            return jsonify({"error": "Missing 'prompt' in request body"}), 400

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 256,
                "do_sample": True
            }
        }

        logging.info("Sending request to Hugging Face API.")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

        logging.info(f"Hugging Face response status: {response.status_code}")
        if response.status_code != 200:
            logging.error(f"Hugging Face API error: {response.text}")
            return jsonify({"error": "Hugging Face API returned an error", "details": response.text}), 500

        try:
            result = response.json()
        except ValueError:
            logging.error("Invalid JSON from Hugging Face API.")
            return jsonify({"error": "Invalid JSON from Hugging Face"}), 500

        if isinstance(result, dict) and result.get("error"):
            logging.error(f"Hugging Face API error field: {result['error']}")
            return jsonify({"error": result["error"]}), 500

        if not isinstance(result, list) or not result or "generated_text" not in result[0]:
            logging.error("Malformed response from Hugging Face.")
            return jsonify({"error": "Unexpected response format"}), 500

        return jsonify({
            "prompt": prompt,
            "code": result[0]["generated_text"]
        })

    except Exception as e:
        logging.exception("Unexpected server error in /analyze.")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
