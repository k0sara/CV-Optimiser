from __future__ import annotations

import re
from collections import Counter

STOPWORDS = {
    "about", "after", "also", "and", "are", "been", "being", "but", "can",
    "for", "from", "have", "into", "its", "job", "more", "our", "role",
    "that", "the", "their", "this", "through", "using", "will", "with", "you",
    "your", "years", "work", "team", "skills", "experience",
}


def normalise_tokens(text: str) -> list[str]:
    return [
        token.lower().strip(".")
        for token in re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#./-]{1,}\b", text)
        if token.lower().strip(".") not in STOPWORDS
    ]


def extract_keywords(job_text: str, limit: int = 24) -> list[str]:
    tokens = normalise_tokens(job_text)
    counts = Counter(tokens)
    first_position = {token: tokens.index(token) for token in counts}
    ranked = sorted(counts, key=lambda token: (-counts[token], first_position[token]))
    return ranked[:limit]


def keyword_match(cv_text: str, job_text: str) -> tuple[list[str], list[str], int]:
    keywords = extract_keywords(job_text)
    cv_tokens = set(normalise_tokens(cv_text))
    strengths = [keyword for keyword in keywords if keyword in cv_tokens]
    missing = [keyword for keyword in keywords if keyword not in cv_tokens]
    score = round(100 * len(strengths) / max(len(keywords), 1))
    return strengths, missing, score


def overall_score(keyword_score: int, ats_readiness: int, content_score: int) -> int:
    return round(keyword_score * 0.60 + ats_readiness * 0.25 + content_score * 0.15)

