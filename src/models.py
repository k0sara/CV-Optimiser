from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ParsedDocument(BaseModel):
    text: str
    page_count: Optional[int] = None
    file_type: str


class ATSCheck(BaseModel):
    name: str
    passed: bool
    detail: str


class BulletSuggestion(BaseModel):
    original: str
    improved: str
    reason: str = ""


class MatchBreakdown(BaseModel):
    keyword_coverage: int = Field(ge=0, le=100)
    ats_readiness: int = Field(ge=0, le=100)
    content_quality: int = Field(ge=0, le=100)


class AnalysisReport(BaseModel):
    match_score: int = Field(ge=0, le=100)
    breakdown: MatchBreakdown
    strengths: list[str]
    missing_skills: list[str]
    ats_checks: list[ATSCheck]
    improved_summary: str
    bullet_suggestions: list[BulletSuggestion]
    projects_to_highlight: list[str]
    suggested_section_order: list[str]
    llm_enhanced: bool = False
