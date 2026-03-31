# 🏥 MedBot Chat – AI Medical Assistant

MedBot Chat is an AI-powered medical chatbot designed to answer healthcare-related questions using a fine-tuned Large Language Model (LLM). The system provides quick, informative, and conversational responses to user queries.
Live Demo

## Try the app here:  
https://huggingface.co/spaces/kzsnlsa/MEDBOT_CHAT

---

## Features

-  Conversational AI chatbot for medical queries  
-  Fine-tuned LLM for domain-specific responses  
-  Fast API using Flask  
-  Docker support for easy deployment  
-  Deployable on hugging space face 
-  Handles general health-related Q&A related to diabetes 

---

## Tech Stack

- **Python**
- **Flask**
- **Hugging Face Transformers**
- **PEFT (Parameter Efficient Fine-Tuning)**
- **BitsAndBytes (for optimized model loading)**
- **Docker**

---

## 📂 Project Structure
MEDBOT_CHAT/
│
├── model/ # Fine-tuned model files
│ ├── adapter_model.safetensors
│ ├── adapter_config.json
│ ├── tokenizer.json
│ └── tokenizer_config.json
│
├── app.py # Main Flask app
├── requirements.txt # Dependencies
├── Dockerfile # Docker setup
├── README.md # Project documentation


---

## Installation & Setup

## Clone the repository

```bash
git clone https://github.com/Heershah99/MEDBOT_CHAT.git
cd MEDBOT_CHAT
pip install -r requirements.txt
python app.py
http://localhost:7860

Deployment
This project is deployed using Hugging Face Spaces.
You can also deploy it on:
Render
Railway
AWS / GCP / Azure

## How It Works
User sends a medical query
Flask API receives the request
Fine-tuned LLM processes the input
Model generates a response
Response is returned to the user


## UI VIEW 
<img width="1882" height="762" alt="image" src="https://github.com/user-attachments/assets/8dc7c365-dc21-4876-83f5-a30bdd0b5878" />
<img width="1896" height="851" alt="image" src="https://github.com/user-attachments/assets/fe988cbf-94f6-4e5a-b327-d7fad42f2ec0" />



