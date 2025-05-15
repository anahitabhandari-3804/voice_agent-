# voice_agent-
# Voice-Based Pre-Screening Tool

## Overview
This project is a Voice-Based Pre-Screening Tool that automates the initial candidate screening process using voice AI technology powered by [Vapi.ai](https://docs.vapi.ai). Recruiters can set up job roles with custom screening questions, and the system automatically calls candidates, asks questions verbally, records and transcribes their responses, evaluates them using simple keyword-based rules, and displays results in a dashboard.

## Features
- **Job Role Creation:** Recruiters can define job titles and add multiple screening questions.
- **Automated Voice Calls:** The system uses Vapi.ai API to call candidates and ask predefined questions.
- **Response Recording & Transcription:** Candidate answers are recorded and transcribed automatically.
- **Simple Evaluation:** Responses are scored based on keyword matching and scoring rules.
- **Dashboard:** Recruiters can view candidate transcripts, evaluation scores, and pass/fail results.
- **Easy to Use Frontend:** Interactive Streamlit interface for recruiters.

## Technology Stack
- Backend: FastAPI (Python)
- Frontend: Streamlit
- Voice API: Vapi.ai (for automated voice calls and transcription)
- Data Storage: JSON files for logs (can be extended to databases)
- HTTP Client: Python requests

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- Vapi.ai API Key ([Get your key here](https://docs.vapi.ai))
- pip package manager

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/voice-pre-screening.git
   cd voice-pre-screening
