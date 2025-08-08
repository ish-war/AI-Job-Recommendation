# AI-Powered Job Recommendation System using LangChain & Gemini

A smart web app that helps students discover suitable job or internship opportunities by matching their skills, experience, and preferences using modern LLM-based Retrieval-Augmented Generation (RAG) techniques.


## Workflow

```
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
