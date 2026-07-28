from __future__ import annotations

import re

from src.models import ATSCheck, ParsedDocument

SECTION_PATTERNS = {
    "experience": r"\b(experience|employment|work history)\b",
    "education": r"\b(education|qualifications)\b",
    "skills": r"\b(skills|technologies|technical skills)\b",
}


def analyse_ats(document: ParsedDocument) -> list[ATSCheck]:
    text = document.text
    words = re.findall(r"\b[\w+#.-]+\b", text)
    checks = [
        ATSCheck(
            name="Email address",
            passed=bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)),
            detail="A recognisable email address is present."
            if re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
            else "Add a professional email address near the top.",
        ),
        ATSCheck(
            name="Phone number",
            passed=bool(re.search(r"(?:\+?\d[\s().-]*){8,}", text)),
            detail="A phone number is present."
            if re.search(r"(?:\+?\d[\s().-]*){8,}", text)
            else "Add a phone number with country code.",
        ),
        ATSCheck(
            name="Standard section headings",
            passed=sum(
                bool(re.search(pattern, text, re.IGNORECASE))
                for pattern in SECTION_PATTERNS.values()
            )
            >= 2,
            detail="Use clear headings such as Experience, Education, and Skills.",
        ),
        ATSCheck(
            name="CV length",
            passed=250 <= len(words) <= 1_200,
            detail=f"Detected {len(words)} words; aim for roughly 250–1,200.",
        ),
    ]
    if document.page_count is not None:
        checks.append(
            ATSCheck(
                name="Page count",
                passed=1 <= document.page_count <= 2,
                detail=f"Detected {document.page_count} page(s); one or two is ideal.",
            )
        )
    return checks


def ats_score(checks: list[ATSCheck]) -> int:
    return round(100 * sum(check.passed for check in checks) / max(len(checks), 1))

