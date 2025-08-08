# app/retriever.py

import os
import json
import hashlib
from groq import Groq
import requests
from typing import List, Dict
from dotenv import load_dotenv

# FAISS + Embeddings
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

load_dotenv()

CACHE_FILE = "cache/job_results_cache.json"
FAISS_INDEX_PATH = "faiss_index"

class JobRetriever:
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.cache = self.load_cache()
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    def load_cache(self):
        if not os.path.exists("cache"):
            os.makedirs("cache")
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_cache(self):
        with open(CACHE_FILE, "w") as f:
            json.dump(self.cache, f, indent=2)

    def generate_cache_key(self, user_input: Dict) -> str:
        combined = f"{user_input['skills']}_{user_input['experience']}_{user_input['location']}_{user_input['job_type']}"
        return hashlib.md5(combined.encode()).hexdigest()

    def _format_user_input(self, user_input: Dict) -> str:
        return (
            f"Find recent job postings relevant to the following profile:\n"
            f"- Skills: {user_input['skills']}\n"
            f"- Experience: {user_input['experience']}\n"
            f"- Preferred location: {user_input['location']}\n"
            f"- Job type: {user_input['job_type']}\n"
            f"Return job title, company, location, and link. Keep it concise."
        )

    def fetch_jobs_with_groq(self, user_input: Dict) -> List[Dict]:
        try:
            query = self._format_user_input(user_input)
            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": query}],
                model="openai/gpt-oss-20b",
                temperature=0.7,
                max_completion_tokens=2048,
                stream=False,
                stop=None,
                tool_choice="required",
                tools=[{"type": "browser_search"}]
            )
            output = response.choices[0].message.content
            print("[GROQ Browser Result]:", output)
            return [{"raw_result": output}]
        except Exception as e:
            print(f"[GROQ Error]: {e}")
            return []

    def fetch_jobs_with_tavily(self, user_input: Dict) -> List[Dict]:
        try:
            search_query = (
                f"{user_input['job_type']} jobs for {user_input['skills']} "
                f"in {user_input['location']} with {user_input['experience']} experience"
            )

            url = "https://api.tavily.com/search"
            payload = {
                "api_key": self.tavily_api_key,
                "query": search_query,
                "search_depth": "basic",
                "include_answer": False,
                "include_images": False,
                "include_raw_content": False,
                "max_results": 5
            }

            response = requests.post(url, json=payload)
            data = response.json()

            results = []
            for item in data.get("results", []):
                results.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "content": item.get("content")
                })

            return results
        except Exception as e:
            print(f"[Tavily Error]: {e}")
            return []

    def _save_faiss_index(self, job_listings: List[Dict]):
        """Save job listings into FAISS index (persistent)"""
        docs = []
        for job in job_listings:
            text = (
                f"Title: {job.get('title', 'N/A')}\n"
                f"URL: {job.get('url', 'N/A')}\n"
                f"Description: {job.get('content', 'No description available.')}"
            )
            docs.append(Document(page_content=text, metadata={"url": job.get("url", "N/A")}))

        if os.path.exists(FAISS_INDEX_PATH):
            # Append to existing index
            existing_index = FAISS.load_local(FAISS_INDEX_PATH, self.embeddings, allow_dangerous_deserialization=True)
            existing_index.add_documents(docs)
            existing_index.save_local(FAISS_INDEX_PATH)
        else:
            # Create new index
            index = FAISS.from_documents(docs, self.embeddings)
            index.save_local(FAISS_INDEX_PATH)

        print(f"[FAISS] Index saved at {FAISS_INDEX_PATH}")

    def get_job_recommendations(self, user_input: Dict) -> List[Dict]:
        cache_key = self.generate_cache_key(user_input)

        if cache_key in self.cache:
            print("[Cache Hit] Returning cached results.")
            jobs = self.cache[cache_key]
        else:
            print("[Cache Miss] Fetching new results...")
            jobs = self.fetch_jobs_with_groq(user_input)

            # Fallback to Tavily if Groq fails
            if not jobs or "raw_result" in jobs[0]:
                jobs = self.fetch_jobs_with_tavily(user_input)

            self.cache[cache_key] = jobs
            self.save_cache()

        # Save results into FAISS index
        if jobs:
            self._save_faiss_index(jobs)

        return jobs
