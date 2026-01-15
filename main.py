import os
import uuid
import requests

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI

# ================== НАСТРОЙКИ ==================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")

VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # стандартный голос ElevenLabs
BASE_URL = "https://linda-ai-dj.onrender.com"

# ================== APP ==================

app = FastAPI()

# 🔴 СТАТИК МОНТИРУЕМ СРАЗУ
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ================== OPENAI ==================

client = OpenAI(api_key=OPENAI_API_KEY)

# ================== MODELS ==================

class Msg(BaseModel):
    message: str

# ================== ROUTES ==================

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/chat")
def chat(data: Msg):
    # --- 1. Запрос к OpenAI ---
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Ты романтичная и заботливая ИИ-девушка по имени Линда."
            },
            {
                "role": "user",
                "content": data.message
            }
        ]
    )

    text = response.choices[0].message.content

    # --- 2. Генерация MP3 через ElevenLabs (ИСПРАВЛЕНО) ---
filename = f"{uuid.uuid4()}.mp3"
file_path = os.path.join("static", filename)

url = 
f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

headers = {
    "xi-api-key": ELEVEN_API_KEY,
    "Accept": "audio/mpeg",
    "Content-Type": "application/json"
}

payload = {
    "text": text,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.4,
        "similarity_boost": 0.8
    }
}

r = requests.post(url, json=payload, headers=headers)
r.raise_for_status()

with open(file_path, "wb") as f:
    f.write(r.content)
