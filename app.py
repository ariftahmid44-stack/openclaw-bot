import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents":[{"parts":[{"text": prompt}]}]
    }
    r = requests.post(url, headers=headers, json=data)
    result = r.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram():
    data = request.json
    message = data["message"]["text"]
    chat_id = data["message"]["chat"]["id"]

    reply = ask_gemini(message)

    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, json={"chat_id": chat_id, "text": reply})

    return "ok"

@app.route("/")
def home():
    return "AANYA AI bot running!"
