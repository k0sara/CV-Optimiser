from src.analyzer import analyse
from src.models import ParsedDocument
from src.reports import markdown_report


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
    assert "CV Optimiser report" in markdown_report(report)


def test_ai_failure_preserves_local_analysis(monkeypatch):
    def unavailable(*args):
        raise RuntimeError("provider unavailable")
    monkeypatch.setattr("src.analyzer.enhance_with_llm", unavailable)
    report = analyse(ParsedDocument(text="Python engineer", file_type="txt"), "Python Docker", use_llm=True)
    assert report.strengths == ["Python"]
    assert report.warnings
    assert not report.llm_enhanced


def test_unknown_role_has_explicit_coverage_warning():
    report = analyse(ParsedDocument(text="Experienced writer", file_type="txt"), "Editorial writer wanted", use_llm=False)
    assert report.warnings
    assert report.breakdown.keyword_coverage == 0

