from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Hugging Face Model API URL
API_URL = "https://api-inference.huggingface.co/models/Salesforce/codegen-350M-multi"

# Hugging Face Token (Environment Variable se lena)
HF_API_KEY = os.getenv("HF_API_KEY")
headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

@app.route('/random')
def home():
    return "CodeGen API (via Hugging Face) ✅"

@app.route('/', methods=['POST'])
def generate_code():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 256,
            "do_sample": True
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        # Error check
        if isinstance(result, dict) and result.get("error"):
            return jsonify({"error": result["error"]}), 500

        generated_text = result[0]["generated_text"]

        return jsonify({
            "prompt": prompt,
            "code": generated_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
