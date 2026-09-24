from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Streamlit executes this file as a script, which can omit the repository root
# from sys.path. Add it explicitly so `streamlit run src/app.py` works from a
# fresh checkout without requiring the package to be installed first.
if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from dotenv import load_dotenv

from src.analyzer import analyse
from src.parser import parse_document

load_dotenv()

st.set_page_config(page_title="CV Optimiser", page_icon="📄", layout="wide")
st.title("CV Optimiser")
st.caption("See how well your CV matches a role—and what to improve next.")

left, right = st.columns(2)
with left:
    cv_file = st.file_uploader("Upload your CV", type=["pdf", "docx", "txt"])
with right:
    job_mode = st.radio("Job description", ["Paste text", "Upload file"], horizontal=True)
    if job_mode == "Paste text":
        job_text = st.text_area("Paste the job description", height=190)
        job_file = None
    else:
        job_file = st.file_uploader(
            "Upload the job description", type=["pdf", "docx", "txt"]
        )
        job_text = ""

use_llm = st.toggle(
    "Use AI writing suggestions",
    value=bool(os.getenv("OPENAI_API_KEY")),
    disabled=not bool(os.getenv("OPENAI_API_KEY")),
    help="Set OPENAI_API_KEY in .env to enable this.",
)

if st.button("Analyse CV", type="primary", use_container_width=True):
    if not cv_file:
        st.error("Please upload your CV.")
    elif not job_text.strip() and not job_file:
        st.error("Please add a job description.")
    else:
        try:
            with st.spinner("Analysing your CV…"):
                cv = parse_document(cv_file.getvalue(), cv_file.name)
                if job_file:
                    job_text = parse_document(
                        job_file.getvalue(), job_file.name
                    ).text
                report = analyse(cv, job_text, use_llm=use_llm)
                st.session_state["report"] = report
        except Exception as error:
            st.error(f"Analysis failed: {error}")

if report := st.session_state.get("report"):
    st.divider()
    score_col, detail_col = st.columns([1, 3])
    with score_col:
        st.metric("Overall match", f"{report.match_score}%")
        st.progress(report.match_score / 100)
        st.caption("AI enhanced" if report.llm_enhanced else "Local analysis")
    with detail_col:
        a, b, c = st.columns(3)
        a.metric("Keyword coverage", f"{report.breakdown.keyword_coverage}%")
        b.metric("ATS readiness", f"{report.breakdown.ats_readiness}%")
        c.metric("Content quality", f"{report.breakdown.content_quality}%")

    strengths_col, missing_col = st.columns(2)
    with strengths_col:
        st.subheader("Strengths")
        st.write("\n".join(f"✓ {item}" for item in report.strengths) or "No clear matches yet.")
    with missing_col:
        st.subheader("Missing keywords")
        st.write("\n".join(f"• {item}" for item in report.missing_skills) or "No major gaps detected.")

    st.subheader("ATS report")
    for check in report.ats_checks:
        icon = "✅" if check.passed else "⚠️"
        st.write(f"{icon} **{check.name}** — {check.detail}")

    st.subheader("Improved professional summary")
    st.info(report.improved_summary)

    st.subheader("Suggested bullet rewrites")
    if report.bullet_suggestions:
        for suggestion in report.bullet_suggestions:
            with st.container(border=True):
                st.caption(f"Original: {suggestion.original}")
                st.write(suggestion.improved)
                st.caption(suggestion.reason)
    else:
        st.write("Use bullet points in the CV to receive line-by-line suggestions.")

    projects_col, order_col = st.columns(2)
    with projects_col:
        st.subheader("What to highlight")
        for item in report.projects_to_highlight:
            st.write(f"• {item}")
    with order_col:
        st.subheader("Suggested section order")
        for index, item in enumerate(report.suggested_section_order, 1):
            st.write(f"{index}. {item}")

    payload = json.dumps(report.model_dump(), indent=2)
    st.download_button(
        "Download report",
        data=payload,
        file_name="cv-analysis-report.json",
        mime="application/json",
        use_container_width=True,
    )
