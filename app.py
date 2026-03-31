from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

app = Flask(__name__)

BASE_MODEL = "EleutherAI/gpt-neox-20b"

tokenizer = AutoTokenizer.from_pretrained("model")

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float16,
    device_map="auto",
    load_in_4bit=True
)

model = PeftModel.from_pretrained(base_model, "model")

@app.route("/")
def home():
    return "NeoX‑20B MedBot API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    user_input = request.json["text"]

    inputs = tokenizer(user_input, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
