import streamlit as st
import requests
import json
from PIL import Image

# Page config with an emoji and a wider layout
st.set_page_config(
    page_title="🎤 Voice Pre-Screening Tool",
    page_icon="🎧",
    layout="wide"
)

# Add a header with custom styles using markdown and emojis
st.markdown("""
<style>
    .title {
        font-size: 3rem;
        font-weight: 700;
        color: #4B8BBE;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.5rem;
        color: #306998;
        text-align: center;
        margin-bottom: 30px;
    }
    .section-header {
        font-size: 1.75rem;
        color: #FFD43B;
        margin-top: 40px;
        margin-bottom: 20px;
        border-bottom: 3px solid #FFD43B;
        padding-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎤 Voice-Based Pre-Screening Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Automate your candidate screening with voice AI</div>', unsafe_allow_html=True)

# Layout the app with two columns for Job Setup and Candidate Call
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<h2 class="section-header">📝 Create Job Role & Questions</h2>', unsafe_allow_html=True)
    with st.form("job_form"):
        job_title = st.text_input("Enter Job Title", placeholder="e.g., Software Engineer")
        questions = st.text_area("Screening Questions (one per line)", placeholder="Write each question on a new line").splitlines()
        submit_job = st.form_submit_button("✅ Create Job")

    if submit_job:
        if job_title and questions:
            with st.spinner("Creating job role..."):
                try:
                    res = requests.post("http://localhost:8000/create-job", json={"job_title": job_title, "screening_questions": questions})
                    if res.status_code == 200:
                        st.success(f"Job '{job_title}' created successfully! 🎉")
                    else:
                        st.error(f"Failed to create job: {res.text}")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")
        else:
            st.warning("Please enter a job title and at least one question.")

with col2:
    st.markdown('<h2 class="section-header">📞 Start Voice Call</h2>', unsafe_allow_html=True)
    with st.form("call_form"):
        phone = st.text_input("Candidate Phone Number", placeholder="+1XXX... (E.164 format)")
        questions_for_call = st.text_area("Questions to Ask (repeat or customize)", placeholder="One question per line").splitlines()
        start_call = st.form_submit_button("📲 Start Call")

    if start_call:
        if phone and questions_for_call:
            with st.spinner("Initiating voice call..."):
                try:
                    res = requests.post("http://localhost:8000/start-call", json={"phone": phone, "questions": questions_for_call})
                    if res.status_code == 200:
                        st.success("Voice call started successfully!")
                        st.json(res.json())
                    else:
                        st.error(f"Call failed: {res.text}")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")
        else:
            st.warning("Please enter candidate phone and questions.")

# Candidate Responses Dashboard
st.markdown('<h2 class="section-header">📋 Candidate Responses Dashboard</h2>', unsafe_allow_html=True)
if st.button("🔄 Refresh Logs"):
    try:
        with open("backend/logs.json") as f:
            logs = json.load(f)
            if not logs:
                st.info("No candidate logs available yet.")
            else:
                for log in logs[::-1]:
                    with st.expander(f"📞 {log['phone']} — {log['job_title']}"):
                        st.markdown(f"**Transcript:** {log['transcript']}")
                        st.markdown(f"**Matched Keywords:** {', '.join(log['evaluation']['matched_keywords'])}")
                        st.markdown(f"**Score:** {log['evaluation']['score']} / {log['evaluation']['total']}")
                        result_icon = "✅" if log["evaluation"]["result"] == "Pass" else "❌"
                        st.markdown(f"**Result:** {result_icon} {log['evaluation']['result']}")
    except FileNotFoundError:
        st.warning("Logs file not found. No responses recorded yet.")
    except Exception as e:
        st.error(f"An error occurred while loading logs: {e}")

# Footer with contact info or help links
st.markdown("""
---
<p style="text-align:center; color:#888; font-size:0.9rem;">
    Developed by Anahita| Powered by Vapi.ai API | For help, contact support@example.com
</p>
""", unsafe_allow_html=True)
