# 💼 AI-Powered Job Recommendation System

An intelligent job recommendation system that uses **Large Language Models (LLMs)** and **web scraping** to find, rank, and recommend jobs based on your skills, experience, and preferences.  
Users can manually enter their details **or** upload a PDF resume, from which the system automatically extracts relevant information using an AI-powered parser.

Built with:
- **Python**
- **Groq LLMs (Gemma and OpenAI Models)**
- **Streamlit** for UI
- **FAISS** for semantic search
- **TAVILY & OPENAI TOOL** for web search 
---

## 🚀 Features

- **AI Resume Parsing** → Extracts skills, experience, and preferences from PDF resumes using Groq LLMs.
- **Web Job Retrieval** → Finds latest job postings matching your profile.
- **Intelligent Recommendations** → Uses semantic similarity + LLM reasoning for ranking jobs.
- **Interactive UI** → Streamlit-based interface for both manual input and resume upload.
- **Configurable** → Supports multiple location preferences, job types, and custom filtering.

---

## 🛠️ Project Structure



## Workflow

```bash
flowchart TD
    %% Style settings
    classDef files fill:#f9f9f9,stroke:#333,stroke-width:1px
    classDef process fill:#d0ebff,stroke:#1c7ed6,stroke-width:1px
    classDef storage fill:#fff3bf,stroke:#f08c00,stroke-width:1px

    %% UI Layer
    A[Streamlit UI (ui/app.py)]:::files -->|Manual input or PDF upload| B[Resume Parser (resume_parser.py)]:::process

    %% Resume Parsing
    B -->|Groq LLM extraction| C[(Parsed Resume Data)]:::storage

    %% Job Retrieval
    C --> D[Job Retriever (retriever.py)]:::process
    D -->|Web scraping / API| E[(Raw Job Postings)]:::storage

    %% Recommendation
    E --> F[Job Recommender (recommender.py)]:::process
    F -->|Semantic Search + LLM Ranking| G[(Ranked Recommendations)]:::storage

    %% Output
    G --> H[Streamlit UI - Display Results]:::files
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/job-recommendation-system.git
cd job-recommendation-system
```
