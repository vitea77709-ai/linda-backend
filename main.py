from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import os
from openai import OpenAI
import requests
import uuid

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

class Msg(BaseModel):
    message: str

@app.post("/chat")
def chat(data: Msg):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Ты романтичная ИИ-девушка по имени Линда. Ты нежная и заботливая."
            },
            {
                "role": "user",
                "content": data.message
            }
        ]
    )

    text = response.choices[0].message.content

    file_name = f"static/{uuid.uuid4()}.mp3"
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

    r = requests.post(url, json=payload, headers=headers)
    with open(file_name, "wb") as f:
        f.write(r.content)

    return {
        "text": text,
        "voice": "/" + file_name
    }
