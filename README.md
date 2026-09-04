# YouTube Compliance Checker - Free Python Version

This is a small, Python-only version of the original `yt-compliance-rag` project.

## What is used

- YouTube Transcript API -> gets available captions
- pypdf -> reads the compliance PDFs
- scikit-learn TF-IDF -> small local RAG/search system
- Ollama -> optional local AI model
- Python -> everything else

## Cost

The project itself has no paid cloud service.

For completely local AI:
1. Install Ollama: https://ollama.com/
2. Open Command Prompt.
3. Run:

    ollama pull llama3.2

4. Keep Ollama running.
5. Run:

    python main.py

If Ollama is not installed/running, the program automatically uses an offline rule-based fallback.

## Windows setup

Open Command Prompt in this folder:

    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt

Then:

    python main.py

## How it works

    YouTube URL
         |
         v
    Transcript
         |
         v
    PDF compliance rules
         |
         v
    TF-IDF similarity search
         |
         v
    Ollama local LLM
         |
         v
    PASS / FAIL
         |
         v
    Violations + evidence + recommendation

## Important limitation

This is a student/demo compliance checker, not a legal compliance system.
A video without captions may not be analyzable by the transcript-only version.
The compliance rules are only as good as the documents placed in `data/`.

## Folder structure

    yt_compliance_free/
    |
    +-- main.py
    +-- transcript_service.py
    +-- rag_engine.py
    +-- llm.py
    +-- compliance.py
    +-- report.py
    +-- requirements.txt
    +-- README.md
    +-- data/
    |   +-- compliance PDF files
    +-- reports/
        +-- generated JSON reports

## Demo

Input:

    https://www.youtube.com/watch?v=VIDEO_ID

Output:

    Status: FAIL

    1. [HIGH] Advertisement / Disclosure
       Problem: ...
       Evidence: ...
       Fix: ...

## Why this is smaller

The original repository uses a LangGraph workflow with Azure services for video indexing, embeddings, vector search and LLM access. This version keeps the same high-level idea—video transcript -> RAG -> compliance decision—but implements it with local Python components. The original repository describes its architecture and Azure-based approach here:

