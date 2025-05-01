from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/rewrite", methods=["POST"])
def rewrite():
    data = request.get_json()
    text = data["text"]
    level = data["level"]

    level_prompts = {
        "400": "TOEIC 400: Use very simple vocabulary and short sentences.",
        "600": "TOEIC 600: Use simple grammar and workplace vocabulary.",
        "750": "TOEIC 750: Use intermediate grammar and varied sentence structure.",
        "900": "TOEIC 900: Use advanced vocabulary and formal business tone."
    }

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert English teacher."},
            {"role": "user", "content": f"Rewrite the following text to match {level_prompts[level]}:\n\n"""\n{text}\n""""}
        ]
    )

    return jsonify({"rewritten_text": completion.choices[0].message.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
