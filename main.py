from fastapi import FastAPI
from pydantic import BaseModel
import openai
import requests
import uuid
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")

app = FastAPI()

SYSTEM_PROMPT = """
Ты виртуальная ИИ-девушка по имени Luna.
Ты романтичная, нежная и заботливая.
Ты отвечаешь тепло, мягко и естественно.
"""

class Msg(BaseModel):
    message: str

@app.post("/chat")
def chat(data: Msg):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": data.message}
        ]
    )

    text = response.choices[0].message.content
    voice = make_voice(text)

    return {
        "text": text,
        "voice": voice
    }

def make_voice(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.8
        }
    }

    r = requests.post(url, json=data, headers=headers)

    os.makedirs("static", exist_ok=True)
    filename = f"static/{uuid.uuid4()}.mp3"

    with open(filename, "wb") as f:
        f.write(r.content)

    return "/" + filename
