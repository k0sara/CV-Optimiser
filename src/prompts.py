SYSTEM_PROMPT = """You are an expert CV editor and ATS specialist.
Return only JSON matching the requested schema. Never invent qualifications,
employers, metrics, or technologies. Rephrase only evidence present in the CV.
Keep suggestions concise, specific, and suitable for a professional CV."""


def analysis_prompt(cv_text: str, job_text: str, missing: list[str]) -> str:
    return f"""Improve this CV for the target job.

CV:
{cv_text[:14000]}

JOB DESCRIPTION:
{job_text[:10000]}

LOCALLY DETECTED MISSING KEYWORDS:
{", ".join(missing[:15])}

Produce an improved summary and up to five bullet rewrites. For each rewrite,
include the original CV line, improved line, and a short reason. Also suggest up
to three evidence-based projects/experiences to highlight. Do not add facts."""

