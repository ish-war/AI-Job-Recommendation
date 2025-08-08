# app/recommender.py

import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

FAISS_INDEX_PATH = "faiss_index"

class JobRecommender:
    def __init__(self):
        # Load embeddings (must match retriever’s model)
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Load FAISS index from disk
        if not os.path.exists(FAISS_INDEX_PATH):
            raise FileNotFoundError(
                f"[ERROR] FAISS index not found at {FAISS_INDEX_PATH}. "
                "Run the retriever first to fetch and index jobs."
            )

        self.vectorstore = FAISS.load_local(
            FAISS_INDEX_PATH,
            self.embeddings,
            allow_dangerous_deserialization=True
        )

        # Initialize Gemini model
        self.llm = ChatGroq(
            model="gemma2-9b-it",
            temperature=0.7
        )

        # Prompt for generating recommendations
        template = """
        You are a smart job recommendation assistant.
        Given the following user profile and a list of job postings, suggest the most relevant ones.

        User Profile:
        {user_profile}

        Job Postings:
        {job_listings}

        Return a short, clear, and helpful recommendation list including:
        - Job Title
        - Why it’s a good fit
        - URL
        """
        self.prompt = PromptTemplate(input_variables=["user_profile", "job_listings"], template=template)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def recommend_jobs(self, user_profile: str, top_k: int = 5) -> str:
        # Search in FAISS index for relevant jobs
        results = self.vectorstore.similarity_search(user_profile, k=top_k)

        # Combine retrieved job listings
        job_text = "\n\n".join([doc.page_content for doc in results])

        # Generate recommendations
        return self.chain.run(user_profile=user_profile, job_listings=job_text)
