from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Initialize app
app = Flask(__name__, template_folder="templates")
CORS(app)

# Load model and tokenizer once on startup
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-2",
    torch_dtype=torch.float32
)

# Generate a response from the local model
def generate_reply(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=200)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    mode = data.get("mode", "explain")
    user_input = data.get("prompt", "")

    if not user_input:
        return jsonify({"reply": "❗ Please enter some code or a topic."})

    # Mode-specific prompts
    if mode == "explain":
        prompt = f"Explain this code in simple terms:\n{user_input}"
    elif mode == "debug":
        prompt = f"Find and fix bugs in this code:\n{user_input}"
    elif mode == "lesson":
        prompt = f"Teach me about: {user_input}"
    elif mode == "quiz":
        prompt = f"Create 3 multiple-choice questions with answers on: {user_input}"
    elif mode == "career":
        prompt = f"Give career advice about: {user_input}"
    else:
        prompt = user_input  # default fallback

    try:
        reply = generate_reply(prompt)
        return jsonify({"reply": reply.strip()})
    except Exception as e:
        return jsonify({"reply": f"❌ Error generating reply: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
