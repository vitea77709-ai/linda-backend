import os
import requests
import io

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI

# ================== KEYS ==================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")

VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

# ================== APP ==================

app = FastAPI()

# ================== MODELS ==================

class ChatRequest(BaseModel):
    message: str

# ================== CLIENT ==================

client = OpenAI(api_key=OPENAI_API_KEY)

# ================== ROUTES ==================

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    # --- OpenAI (текст) ---
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Ты милая романтичная девушка по имени Линда"
            },
            {
                "role": "user",
                "content": req.message
            }
        ]
    )

    ai_reply = completion.choices[0].message.content

    # --- ElevenLabs (голос) ---
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    payload = {
        "text": ai_reply,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.7
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        return {
            "error": "ElevenLabs error",
            "details": response.text
        }

    audio_bytes = response.content

    return StreamingResponse(
        io.BytesIO(audio_bytes),
        media_type="audio/mpeg",
        headers={
            "X-AI-Text": ai_reply
        }
    )
