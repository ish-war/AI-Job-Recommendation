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
```bash
├── app
│ ├── init.py
│ ├── recommender.py # Ranks and explains job recommendations
│ ├── retriever.py # Retrieves job postings from the web
│ ├── resume_parser.py # AI-based resume data extraction
│ ├── utils.py # Utility functions (currently placeholder)
│
├── cache # Stores cached results
├── faiss_index # FAISS index for semantic search
├── tests # Unit tests
│
├── ui
│ ├── app.py # Streamlit UI
│
├── main.py # CLI entry point (non-UI execution)
├── requirements.txt
├── README.md
├── sample_resume.pdf # Sample resume for testing
└── .env # Environment variables (Groq API keys, etc.)
```

## Workflow

<img width="356" height="1440" alt="jobrecom mermaid" src="https://github.com/user-attachments/assets/5c2476b8-f73d-4f61-8789-c735f3594c07" />

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/ish-war/AI-Job-Recommendation.git
cd job-recommendation-system
```
### 2️⃣ Create and activate virtual environment
```bash
uv init
uv venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies
```bash
uv add -r requirements.txt
```

### 4️⃣ Set up environment variables

Create a .env file in the root directory:
```bash
GROQ_API_KEY = your_groq_api_key_here
TAVILY_API_KEY = your_tavily_api_key_here
```

### ▶️ Running the Application

```bash
streamlit run ui/app.py       # Run with Streamlit UI
python main.py     # Run via CLI (for testing)
```

## 📥 Usage

### Option 1 – Manual Input

* Enter your skills, experience, and preferences in the form.

* Click Find Jobs to see recommendations.

### Option 2 – Resume Upload

* Upload a PDF resume.

* The AI-powered parser will extract your details automatically.

* Click Find Jobs.

## Web Interface 

<img width="1599" height="897" alt="Screenshot 2025-08-08 232231" src="https://github.com/user-attachments/assets/6584a8b0-0bb1-46c7-b385-b7278cefd1be" />
<img width="1599" height="897" alt="Screenshot 2025-08-08 232308" src="https://github.com/user-attachments/assets/70bfe24d-83a0-489a-9912-767d6a18dc0e" />


## 🤝 Contributing

Pull requests are welcome!

Please open an issue first to discuss major changes.

## 📜 License

This project is licensed under the MIT License.
