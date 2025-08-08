# src/resume_parser.py

import os
from PyPDF2 import PdfReader
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

class ResumeParser:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def extract_text_from_pdf(self, file) -> str:
        """Extract all text from a PDF file."""
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text

    def extract_from_resume(self, file):
        """Use Groq LLM to parse resume and extract structured details."""
        text = self.extract_text_from_pdf(file)

        prompt = f"""
        You are a resume parsing assistant.
        Extract the following details from the resume text below and return ONLY a valid JSON object:
        - skills: a comma-separated list of core technical skills
        - experience: total years of professional experience (numeric with 'years')
        - location: likely city or region of the candidate
        - job_type: one of [Full-time, Part-time, Internship, Contract, Remote] if mentioned, else "Not Found"

        Resume Text:
        {text}

        Respond in JSON format only, example:
        {{
            "skills": "Python, SQL, Machine Learning",
            "experience": "3 years",
            "location": "San Francisco",
            "job_type": "Full-time"
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model="gemma2-9b-it",  # Using Gemma via Groq
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_completion_tokens=512
            )

            raw_output = response.choices[0].message.content.strip()

            # Ensure valid JSON
            details = json.loads(raw_output)
            return details

        except Exception as e:
            print(f"[Groq Resume Parsing Error]: {e}")
            return {
                "skills": "Not Found",
                "experience": "Not Found",
                "location": "Not Found",
                "job_type": "Not Found"
            }

