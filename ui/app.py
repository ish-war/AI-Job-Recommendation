# app.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from dotenv import load_dotenv
from src.resume_parser import ResumeParser
from src.retriever import JobRetriever
from src.recommender import JobRecommender

load_dotenv()

FAISS_INDEX_PATH = "faiss_index"

st.set_page_config(page_title="AI Job Finder", layout="wide")

st.title("💼 AI-Powered Job Finder")
st.markdown("Upload your resume or fill in your details to get personalized job recommendations.")

# --- Step 1: Resume Upload & Parsing ---
resume_parser = ResumeParser()
parsed_data = {}

uploaded_file = st.file_uploader("📄 Upload your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting details from your resume..."):
        parsed_data = resume_parser.extract_from_resume(uploaded_file)
    st.success("✅ Resume parsed successfully!")

# --- Step 2: Input Form ---
with st.form("job_input_form"):
    skills = st.text_input(
        "Skills",
        value=parsed_data.get("skills", "")
    )
    experience = st.text_input(
        "Experience",
        value=parsed_data.get("experience", "")
    )
    location = st.text_input(
        "Preferred Location",
        value=parsed_data.get("location", "")
    )
    job_type = st.selectbox(
        "Job Type",
        options=["Full-time", "Part-time", "Internship", "Contract", "Remote", "Not Found"],
        index=(
            ["Full-time", "Part-time", "Internship", "Contract", "Remote", "Not Found"]
            .index(parsed_data.get("job_type", "Full-time"))
            if parsed_data else 0
        )
    )

    submit_btn = st.form_submit_button("🔍 Find Jobs")

# --- Step 3: Job Retrieval + Recommendations ---
if submit_btn:
    user_input = {
        "skills": skills,
        "experience": experience,
        "location": location,
        "job_type": job_type
    }

    with st.spinner("Fetching job listings..."):
        retriever = JobRetriever()
        retriever.get_job_recommendations(user_input)

    user_profile_str = f"{experience} experience with skills in {skills}, preferring {job_type} roles in {location}."

    with st.spinner("Generating recommendations..."):
        recommender = JobRecommender()
        recommendations = recommender.recommend_jobs(user_profile_str, top_k=5)

    st.subheader("🎯 Recommended Jobs")
    st.write(recommendations)

# --- Footer ---
st.markdown("---")
st.caption("Powered by Groq LLM + Tavily Search + FAISS Vector DB")
