"""Portable, human-readable report export without additional dependencies."""
from src.models import AnalysisReport


def markdown_report(report: AnalysisReport) -> str:
    lines = ["# CV Optimiser report", "", f"Overall match: {report.match_score}/100", "",
             "This heuristic score is a revision aid, not a hiring prediction.", "",
             "## Score breakdown", "",
             f"- Skill coverage: {report.breakdown.keyword_coverage}% (60% weight)",
             f"- ATS checks: {report.breakdown.ats_readiness}% (25% weight)",
             f"- Content signals: {report.breakdown.content_quality}% (15% weight)", ""]
    for warning in report.warnings:
        lines += [f"> {warning}", ""]
    lines += ["## Skill evidence", ""]
    for item in report.skill_evidence:
        lines += [f"- {'Matched' if item.matched else 'Missing'}: {item.skill} ({item.priority})"]
        if item.evidence:
            lines += [f"  Evidence: {item.evidence}"]
    lines += ["", "## ATS checks", ""]
    lines += [f"- {'Pass' if check.passed else 'Review'} — {check.name}: {check.detail}" for check in report.ats_checks]
    lines += ["", "## Summary guidance", "", report.improved_summary, "", "## Bullet suggestions", ""]
    for item in report.bullet_suggestions:
        lines += [f"Original: {item.original}", "", f"Suggestion: {item.improved}", "", item.reason, ""]
    lines += ["## What to highlight", ""] + [f"- {item}" for item in report.projects_to_highlight]
    lines += ["", "## Suggested section order", ""] + [f"{i}. {item}" for i, item in enumerate(report.suggested_section_order, 1)]
    return "\n".join(lines) + "\n"
