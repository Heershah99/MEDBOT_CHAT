import os
import traceback
import torch
from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

app = Flask(__name__)

HF_MODEL_ID = "kzsnlsa/medbot-model"
PORT = int(os.getenv("PORT", 7860))
HOST = "0.0.0.0"
MAX_TOKENS = 512

model = None
tokenizer = None
device = "cuda" if torch.cuda.is_available() else "cpu"


def load_model():
    global model, tokenizer
    if model is not None and tokenizer is not None:
        return

    print(f"Loading model from Hugging Face: {HF_MODEL_ID} on {device}")

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16
    )

    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neox-20b")
    tokenizer.pad_token = tokenizer.eos_token

    base_model = AutoModelForCausalLM.from_pretrained(
        "EleutherAI/gpt-neox-20b",
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )

    model = PeftModel.from_pretrained(base_model, HF_MODEL_ID)
    model.eval()
    print("Model loaded successfully.")


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    try:
        load_model()

        data = request.json or {}
        prompt = data.get("prompt", "").strip()
        max_new_tokens = int(data.get("max_new_tokens", MAX_TOKENS))
        temperature = float(data.get("temperature", 0.7))
        top_p = float(data.get("top_p", 0.9))

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # -----------------------------
        # SYSTEM PROMPT GOES HERE
        # -----------------------------
        system_prompt = (
            "You are MedBot, a concise medical information assistant. "
            "You answer in short, clear paragraphs. "
            "You avoid repetition. "
            "You do not tell personal stories. "
            "You do not invent patient histories. "
            "You only explain medical concepts in simple terms."
        )

        full_prompt = f"{system_prompt}\nUser: {prompt}\nMedBot:"

        inputs = tokenizer(full_prompt, return_tensors="pt").to(device)

        with torch.no_grad():
            outputs = model.generate(
                input_ids=inputs["input_ids"],
                max_new_tokens=80,
                temperature=temperature,
                top_p=top_p,
                top_k=50,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )

        response = tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[1]:],
            skip_special_tokens=True
        )

        return jsonify({"response": response}), 200

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    load_model()
    app.run(host=HOST, port=PORT)
