from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from src.analyzer import analyse
from src.models import AnalysisReport
from src.parser import UnsupportedFileType, parse_document

app = FastAPI(title="CV Optimiser API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyse", response_model=AnalysisReport)
async def analyse_cv(
    cv_file: UploadFile = File(...),
    job_text: Optional[str] = Form(None),
    job_file: Optional[UploadFile] = File(None),
    use_llm: bool = Form(True),
) -> AnalysisReport:
    try:
        cv = parse_document(await cv_file.read(), cv_file.filename or "cv.pdf")
        description = job_text or ""
        if job_file is not None:
            parsed_job = parse_document(
                await job_file.read(), job_file.filename or "job.txt"
            )
            description = parsed_job.text
        return analyse(cv, description, use_llm=use_llm)
    except (UnsupportedFileType, ValueError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
