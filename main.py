# main.py

import os
from dotenv import load_dotenv
from src.retriever import JobRetriever
from src.recommender import JobRecommender

load_dotenv()

FAISS_INDEX_PATH = "faiss_index"

def main():
    # Step 1: Define user profile
    user_input = {
        "skills": "Python, Machine Learning, SQL",
        "experience": "2 years",
        "location": "Remote or Bangalore",
        "job_type": "Full-time"
    }

    # Step 2: Check if FAISS index exists, else run retriever to fetch & index jobs
    if not os.path.exists(FAISS_INDEX_PATH):
        print("[INFO] No FAISS index found — running retriever to fetch and store jobs...")
        retriever = JobRetriever()
        retriever.get_job_recommendations(user_input)
    else:
        print("[INFO] Found existing FAISS index — skipping job fetching.")

    # Step 3: Format user profile string for recommendations
    user_profile_str = (
        f"{user_input['experience']} experience with skills in {user_input['skills']}, "
        f"preferring {user_input['job_type']} roles in {user_input['location']}."
    )

    # Step 4: Generate recommendations
    recommender = JobRecommender()
    recommendations = recommender.recommend_jobs(user_profile_str, top_k=5)

    # Step 5: Display output
    print("\n🎯 Recommended Jobs:\n")
    print(recommendations)

if __name__ == "__main__":
    main()
