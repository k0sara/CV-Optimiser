from __future__ import annotations

import re

from src.ats import analyse_ats, ats_score
from src.llm import enhance_with_llm
from src.models import (
    AnalysisReport,
    BulletSuggestion,
    MatchBreakdown,
    ParsedDocument,
)
from src.scoring import keyword_match, overall_score


def analyse(cv: ParsedDocument, job_text: str, use_llm: bool = True) -> AnalysisReport:
    if not cv.text.strip():
        raise ValueError("No readable text was found in the CV.")
    if not job_text.strip():
        raise ValueError("The job description is empty.")

    strengths, missing, keyword_score = keyword_match(cv.text, job_text)
    checks = analyse_ats(cv)
    readiness = ats_score(checks)
    content_score = _content_score(cv.text)
    enhancement = enhance_with_llm(cv.text, job_text, missing) if use_llm else None

    summary = (
        enhancement.improved_summary
        if enhancement
        else _local_summary(strengths, missing)
    )
    bullets = (
        enhancement.bullet_suggestions
        if enhancement
        else _local_bullet_suggestions(cv.text)
    )
    projects = (
        enhancement.projects_to_highlight
        if enhancement
        else _local_project_suggestions(strengths)
    )

    return AnalysisReport(
        match_score=overall_score(keyword_score, readiness, content_score),
        breakdown=MatchBreakdown(
            keyword_coverage=keyword_score,
            ats_readiness=readiness,
            content_quality=content_score,
        ),
        strengths=_display_terms(strengths[:12]),
        missing_skills=_display_terms(missing[:12]),
        ats_checks=checks,
        improved_summary=summary,
        bullet_suggestions=bullets,
        projects_to_highlight=projects,
        suggested_section_order=[
            "Contact information",
            "Professional summary",
            "Technical skills",
            "Professional experience",
            "Projects",
            "Education",
            "Certifications",
        ],
        llm_enhanced=enhancement is not None,
    )


def _content_score(text: str) -> int:
    bullet_lines = [
        line for line in text.splitlines() if re.match(r"^\s*[-•*]", line)
    ]
    action_verbs = re.findall(
        r"\b(built|created|delivered|developed|improved|increased|led|reduced|"
        r"implemented|designed|automated|managed|analysed|analyzed)\b",
        text,
        re.IGNORECASE,
    )
    metrics = re.findall(r"\b\d+(?:\.\d+)?%|\b(?:£|\$|€)\s?\d+", text)
    return min(100, 45 + min(len(bullet_lines), 10) * 3 + min(len(action_verbs), 8) * 3 + min(len(metrics), 4) * 2)


def _local_summary(strengths: list[str], missing: list[str]) -> str:
    if strengths:
        skills = ", ".join(_display_terms(strengths[:5]))
        return (
            f"Results-focused professional with relevant experience across {skills}. "
            "Apply the strongest evidence and measurable outcomes from the CV to "
            "show direct fit for this role."
        )
    return (
        "Add a concise 3–4 line summary that names the target role, strongest "
        "relevant skills, years or scope of experience, and one measurable result."
    )


def _local_bullet_suggestions(text: str) -> list[BulletSuggestion]:
    candidates = [
        line.strip().lstrip("-•* ").strip()
        for line in text.splitlines()
        if re.match(r"^\s*[-•*]", line) and len(line.strip()) > 20
    ][:5]
    return [
        BulletSuggestion(
            original=line,
            improved=f"{line.rstrip('.')}; add the scale, action, and measurable result.",
            reason="Strong bullets show what changed because of your work.",
        )
        for line in candidates
    ]


def _local_project_suggestions(strengths: list[str]) -> list[str]:
    shown = _display_terms(strengths[:4])
    if not shown:
        return ["Highlight the project or role most closely related to the job."]
    return [
        f"Move the strongest project using {skill} closer to the top."
        for skill in shown[:3]
    ]


def _display_terms(terms: list[str]) -> list[str]:
    aliases = {"sql": "SQL", "aws": "AWS", "api": "API", "ui": "UI", "ml": "ML"}
    return [aliases.get(term, term.title()) for term in terms]

