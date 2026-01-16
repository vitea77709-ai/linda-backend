import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # стандартный голос
AUDIO_FILE = "speech.mp3"

app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/speak")
def speak(text: str):
    if not ELEVENLABS_API_KEY:
        raise HTTPException(status_code=500, detail="API key not set")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.7
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"ElevenLabs error: {response.text}"
        )

    with open(AUDIO_FILE, "wb") as f:
        f.write(response.content)

    return FileResponse(
        AUDIO_FILE,
        media_type="audio/mpeg",
        filename="speech.mp3"
    )
