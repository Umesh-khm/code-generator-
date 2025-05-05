@app.route('/analyze', methods=['POST'])  # 🔁 Renamed from /generate
def analyze_code():
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
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        # Log the raw response text (for debugging)
        print(f"Raw response from Hugging Face: {response.text}")

        try:
            result = response.json()
        except ValueError:
            return jsonify({"error": f"Invalid JSON received from Hugging Face. Raw Response: {response.text}"}), 500

        if isinstance(result, dict) and result.get("error"):
            return jsonify({"error": result["error"]}), 500

        if not isinstance(result, list) or len(result) == 0 or "generated_text" not in result[0]:
            return jsonify({"error": "No generated text in response"}), 500

        generated_text = result[0]["generated_text"]

        return jsonify({
            "prompt": prompt,
            "code": generated_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
