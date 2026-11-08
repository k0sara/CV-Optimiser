from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


OUTPUT = Path(__file__).resolve().parents[1] / "sample_data" / "Alex_Morgan_Sample_CV.docx"
NAVY = RGBColor(22, 52, 79)
DARK = RGBColor(30, 35, 40)
MUTED = RGBColor(85, 95, 105)


def set_font(run, size=10.5, bold=False, color=DARK, italic=False):
    run.font.name = "Arial"
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), "Arial")
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), "Arial")
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color


def set_bottom_border(paragraph, color="16344F", size="10"):
    p_pr = paragraph._p.get_or_add_pPr()
    borders = p_pr.find(qn("w:pBdr"))
    if borders is None:
        borders = OxmlElement("w:pBdr")
        p_pr.append(borders)
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), size)
    bottom.set(qn("w:space"), "4")
    bottom.set(qn("w:color"), color)
    borders.append(bottom)


def set_repeat_keep(paragraph):
    p_pr = paragraph._p.get_or_add_pPr()
    p_pr.append(OxmlElement("w:keepNext"))


def configure_styles(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = DARK
    normal.paragraph_format.space_after = Pt(3)
    normal.paragraph_format.line_spacing = 1.08

    h1 = doc.styles["Heading 1"]
    h1.font.name = "Arial"
    h1._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    h1._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    h1.font.size = Pt(11.5)
    h1.font.bold = True
    h1.font.color.rgb = NAVY
    h1.paragraph_format.space_before = Pt(9)
    h1.paragraph_format.space_after = Pt(4)
    h1.paragraph_format.keep_with_next = True

    bullet = doc.styles["List Bullet"]
    bullet.font.name = "Arial"
    bullet._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    bullet._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    bullet.font.size = Pt(10.2)
    bullet.paragraph_format.left_indent = Inches(0.22)
    bullet.paragraph_format.first_line_indent = Inches(-0.16)
    bullet.paragraph_format.space_after = Pt(2)
    bullet.paragraph_format.line_spacing = 1.04


def add_section_heading(doc, text):
    paragraph = doc.add_paragraph(text.upper(), style="Heading 1")
    set_bottom_border(paragraph, color="A9BBC9", size="5")
    return paragraph


def add_role(doc, title, company, dates):
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(3)
    paragraph.paragraph_format.space_after = Pt(1)
    paragraph.paragraph_format.keep_with_next = True
    set_repeat_keep(paragraph)
    set_font(paragraph.add_run(title), size=10.5, bold=True, color=NAVY)
    set_font(paragraph.add_run(f"  |  {company}"), size=10.5, bold=True)
    if dates:
        set_font(paragraph.add_run(f"  |  {dates}"), size=9.5, color=MUTED)


def add_bullets(doc, items):
    for item in items:
        paragraph = doc.add_paragraph(style="List Bullet")
        paragraph.paragraph_format.keep_together = True
        set_font(paragraph.add_run(item), size=10.2)


def add_compact_line(doc, label, value):
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(1.5)
    set_font(paragraph.add_run(f"{label}: "), size=10.2, bold=True, color=NAVY)
    set_font(paragraph.add_run(value), size=10.2)


def build_cv():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.55)
    section.bottom_margin = Inches(0.55)
    section.left_margin = Inches(0.72)
    section.right_margin = Inches(0.72)
    section.header_distance = Inches(0.3)
    section.footer_distance = Inches(0.3)
    configure_styles(doc)

    name = doc.add_paragraph()
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    name.paragraph_format.space_after = Pt(2)
    set_font(name.add_run("ALEX MORGAN"), size=23, bold=True, color=NAVY)

    contact = doc.add_paragraph()
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact.paragraph_format.space_after = Pt(8)
    set_font(
        contact.add_run(
            "Sofia, Bulgaria  •  alex.morgan@example.com  •  Phone: [sample number]\n"
            "Portfolio: https://example.com/alex-morgan  •  Fictional contact details"
        ),
        size=9.3,
        color=MUTED,
    )

    add_section_heading(doc, "Professional Summary")
    summary = doc.add_paragraph(
        "Backend-focused Software Engineer with 3 years of experience building "
        "Python applications, REST APIs, and data-processing services. Experienced "
        "with FastAPI, PostgreSQL, SQL, AWS, automated testing, and CI/CD. "
        "Comfortable collaborating with product and engineering teams to deliver "
        "reliable software and improve development workflows."
    )
    summary.paragraph_format.space_after = Pt(3)

    add_section_heading(doc, "Technical Skills")
    add_compact_line(doc, "Languages", "Python, SQL, JavaScript")
    add_compact_line(doc, "Frameworks", "FastAPI, Flask, React")
    add_compact_line(doc, "Databases", "PostgreSQL, MySQL, Redis")
    add_compact_line(doc, "Cloud & DevOps", "AWS, GitHub Actions, Docker")
    add_compact_line(doc, "Testing & Tools", "Pytest, unit testing, integration testing, Git, Linux, Jira, Postman")

    add_section_heading(doc, "Professional Experience")
    add_role(doc, "Software Engineer", "Bright Data Solutions, Sofia", "Mar 2023 – Present")
    add_bullets(
        doc,
        [
            "Developed Python and FastAPI services that process more than 500,000 customer records per day.",
            "Designed REST API endpoints used by three internal applications.",
            "Improved PostgreSQL query performance by 35% through indexing and query optimisation.",
            "Built automated test suites with Pytest, increasing backend test coverage from 55% to 82%.",
            "Created GitHub Actions workflows for automated testing and deployment.",
            "Deployed application services to AWS and monitored production performance.",
            "Collaborated with frontend developers and product managers during two-week Agile sprints.",
            "Documented API endpoints and technical decisions for other engineering teams.",
        ],
    )

    add_role(doc, "Junior Software Developer", "Northstar Technologies, Sofia", "Jun 2021 – Feb 2023")
    add_bullets(
        doc,
        [
            "Built internal Python tools that reduced manual reporting work by approximately eight hours per week.",
            "Maintained Flask applications used by finance and operations teams.",
            "Created SQL reports and dashboards based on PostgreSQL data.",
            "Investigated application errors and resolved more than 40 support tickets.",
            "Participated in code reviews and helped improve team coding standards.",
            "Integrated third-party APIs for payment and customer-notification services.",
        ],
    )

    add_section_heading(doc, "Projects")
    add_role(doc, "Job Application Tracker", "Personal Project", "")
    add_bullets(
        doc,
        [
            "Created a full-stack application using FastAPI, React, and PostgreSQL.",
            "Implemented authentication, job tracking, search, and reporting features.",
            "Added automated tests and deployed the application to AWS.",
        ],
    )
    add_role(doc, "Sales Forecasting Pipeline", "Personal Project", "")
    add_bullets(
        doc,
        [
            "Built a Python data pipeline that cleans and analyses historical sales data.",
            "Created scheduled reports that reduced monthly preparation time by 60%.",
            "Presented project results to technical and non-technical stakeholders.",
        ],
    )

    add_section_heading(doc, "Education & Certifications")
    education = doc.add_paragraph()
    education.paragraph_format.space_after = Pt(1.5)
    set_font(education.add_run("BSc Computer Science"), size=10.3, bold=True, color=NAVY)
    set_font(education.add_run("  |  Sofia University  |  2017 – 2021"), size=10.3)
    add_compact_line(
        doc,
        "Certifications",
        "AWS Certified Cloud Practitioner; Professional Scrum Master I",
    )
    add_compact_line(doc, "Languages", "English – Fluent; Bulgarian – Native")

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_font(
        footer.add_run("Alex Morgan  •  Sample CV for CV Optimiser testing"),
        size=8,
        color=MUTED,
    )

    doc.core_properties.title = "Alex Morgan – Sample CV"
    doc.core_properties.subject = "Sample CV for CV Optimiser testing"
    doc.core_properties.author = "CV Optimiser"
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    build_cv()
