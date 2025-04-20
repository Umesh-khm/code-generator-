# code-generator-
from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load Hugging Face model
codegen = pipeline("text-generation", model="Salesforce/codegen-350M-multi")

@app.route('/')
def home():
    return "CodeGen API is Running ✅"

@app.route('/generate', methods=['POST'])
def generate_code():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    result = codegen(prompt, max_length=256, do_sample=True)[0]['generated_text']
    return jsonify({
        "prompt": prompt,
        "code": result
    })

if __name__ == "__main__":
    app.run(debug=True)

