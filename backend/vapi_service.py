
import requests
import os
from dotenv import load_dotenv

load_dotenv()
VAPI_PRIVATE_KEY = os.getenv("VAPI_PRIVATE_KEY")

def create_and_start_agent(candidate_number: str, questions: list):
    url = "https://api.vapi.ai/call"
    headers = {
        "Authorization": f"Bearer {VAPI_PRIVATE_KEY}",
        "Content-Type": "application/json"
    }
    script = "\n".join(questions)
    payload = {
        "phoneNumber": candidate_number,
        "voice": "olivia",
        "message": f"Hello! I'm calling for your screening.\n{script}\nThank you for your time.",
        "transcription": {
            "enabled": True,
            "mode": "full"
        },
        "webhook": {
            "url": "http://localhost:8000/receive-transcription"
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()
