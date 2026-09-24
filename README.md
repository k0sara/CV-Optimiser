# CV Optimiser

CV Optimiser compares a CV with a job description and returns a structured,
ATS-aware report. The first version works locally without an API key; adding an
OpenAI key enables richer summary and bullet rewrites.

## Features

- PDF, DOCX, and TXT parsing
- Overall match score and keyword coverage
- Strong and missing skills
- Deterministic ATS checks
- Suggested CV section order and projects to highlight
- Optional LLM-generated summary and bullet rewrites
- Streamlit UI and FastAPI endpoint

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

The UI opens at `http://localhost:8501`.

Running `streamlit run src/app.py` is also supported.

To run the API instead:

```bash
uvicorn src.api:app --reload
```

Then open `http://localhost:8000/docs`. The `POST /analyse` endpoint accepts
`cv_file` plus either `job_text` or `job_file`.

## Tests

```bash
pytest
```

## Architecture

```text
Upload → Parser → ATS checks ─┐
                 Keywords ────┼→ Scoring → Structured report → UI/API
                 Optional LLM ┘
```

The local analyser is intentionally deterministic and explainable. The LLM is
used only to enrich writing suggestions and must return validated JSON.
