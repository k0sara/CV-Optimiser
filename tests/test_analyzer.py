from src.analyzer import analyse
from src.models import ParsedDocument


def test_analysis_returns_structured_report_without_llm():
    cv = ParsedDocument(
        text="""Jane Doe
jane@example.com | +359 888 123 456
SKILLS
Python, SQL
EXPERIENCE
- Built a Python service that improved processing by 30%.
EDUCATION
BSc Computer Science
""" * 5,
        page_count=1,
        file_type="pdf",
    )
    report = analyse(
        cv,
        "We need a Python engineer with SQL, Docker and Kubernetes.",
        use_llm=False,
    )
    assert 0 <= report.match_score <= 100
    assert "Python" in report.strengths
    assert "Docker" in report.missing_skills
    assert report.llm_enhanced is False
    assert report.ats_checks

