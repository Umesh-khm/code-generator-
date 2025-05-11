from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-generation", model="Salesforce/codegen-350M-multi")


# ✅ Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

app = Flask(__name__)

# ✅ HIGHLIGHTED CHANGE — CORS now restricted to your GitHub Pages frontend
CORS(app, methods=["GET", "POST", "OPTIONS"])


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
            "code": pipe(prompt)
        }

        return payload


    except Exception as e:
        logging.exception("Unexpected server error in /analyze.")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
