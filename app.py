import os
import io
import requests

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from openai import OpenAI

# ================== НАСТРОЙКИ ==================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")

VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

# ================== APP ==================

app = FastAPI()
client = OpenAI(api_key=OPENAI_API_KEY)

# ================== ROUTES ==================

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/speak")
def speak(text: str):
    # ---------- OpenAI ----------
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты милая романтичная девушка по имени Линда"},
            {"role": "user", "content": text}
        ]
    )

    ai_reply = completion.choices[0].message.content

    # ---------- ElevenLabs ----------
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    payload = {
        "text": ai_reply,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.7
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    # ---------- ОТЛАДКА ----------
    # Если пришло НЕ аудио — покажем ошибку
    content_type = response.headers.get("Content-Type", "")

    if "audio" not in content_type:
        return JSONResponse({
            "error": "ElevenLabs did not return audio",
            "status_code": response.status_code,
            "content_type": content_type,
            "response_text": response.text
        })

    # ---------- AUDIO STREAM ----------
    return StreamingResponse(
        io.BytesIO(response.content),
        media_type="audio/mpeg"
    )
