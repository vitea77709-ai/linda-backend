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
def chat(req: ChatRequest):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты милая девушка по имени Линда"},
            {"role": "user", "content": req.message}
        ]
    )

    ai_reply = completion.choices[0].message.content

    text = ai_reply
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.7
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    filename = f"static/{uuid.uuid4()}.mp3"
    with open(filename, "wb") as f:
        f.write(response.content)

    return {
        "text": ai_reply,
        "audio": f"{BASE_URL}/{filename}"
    }

   # ===== ELEVENLABS =====

text = ai_reply  # ВАЖНО! объявляем переменную

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

headers = {
    "xi-api-key": ELEVEN_API_KEY,
    "Content-Type": "application/json"
}

payload = {
    "text": text,
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.7
    }
}

response = requests.post(url, json=payload, headers=headers)

filename = f"static/{uuid.uuid4()}.mp3"

with open(filename, "wb") as f:
    f.write(response.content)
