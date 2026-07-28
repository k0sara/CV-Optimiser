from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI
from pydantic import BaseModel

from src.models import BulletSuggestion
from src.prompts import SYSTEM_PROMPT, analysis_prompt


class LLMEnhancement(BaseModel):
    improved_summary: str
    bullet_suggestions: list[BulletSuggestion]
    projects_to_highlight: list[str]


def enhance_with_llm(
    cv_text: str, job_text: str, missing: list[str]
) -> Optional[LLMEnhancement]:
    if not os.getenv("OPENAI_API_KEY"):
        return None
    client = OpenAI()
    response = client.responses.parse(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": analysis_prompt(cv_text, job_text, missing)},
        ],
        text_format=LLMEnhancement,
    )
    return response.output_parsed
