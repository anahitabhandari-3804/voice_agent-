from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests

app = FastAPI()

# Enable CORS for local testing (adjust in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store (for demo)
jobs = {}
logs = []

class JobRequest(BaseModel):
    job_title: str
    screening_questions: list[str]

class CallRequest(BaseModel):
    phone: str
    questions: list[str]

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
        "transcription": {"enabled": True, "mode": "full"},
        "webhook": {"url": "https://your-server.com/receive-transcription"}  # Replace with your webhook
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

@app.post("/create-job")
def create_job(req: JobRequest):
    jobs[req.job_title] = req.screening_questions
    return {"message": f"Job '{req.job_title}' created"}

@app.post("/start-call")
def start_call(req: CallRequest):
    try:
        vapi_response = create_and_start_agent(req.phone, req.questions)
        # Simulated evaluation — replace with real logic after webhook transcription
        evaluation = {
            "matched_keywords": ["python", "ai"], 
            "score": 8,
            "total": 10,
            "result": "Pass"
        }
        logs.append({
            "phone": req.phone,
            "job_title": "Unknown Job",  # Optionally pass job title to frontend
            "transcript": "Simulated transcript from candidate response.",
            "evaluation": evaluation
        })
        return {"vapi_response": vapi_response, "evaluation": evaluation}
    except Exception as e:
        return {"error": str(e)}

@app.get("/get-logs")
def get_logs():
    return logs
