from __future__ import annotations

from io import BytesIO
from pathlib import Path

import fitz
from docx import Document

from src.models import ParsedDocument


class UnsupportedFileType(ValueError):
    pass


def parse_document(data: bytes, filename: str) -> ParsedDocument:
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf":
        return _parse_pdf(data)
    if suffix == ".docx":
        return _parse_docx(data)
    if suffix in {".txt", ".md"}:
        return ParsedDocument(
            text=data.decode("utf-8", errors="replace").strip(),
            page_count=None,
            file_type=suffix.removeprefix("."),
        )
    raise UnsupportedFileType(
        f"Unsupported file type '{suffix or 'unknown'}'. Use PDF, DOCX, or TXT."
    )


def _parse_pdf(data: bytes) -> ParsedDocument:
    with fitz.open(stream=data, filetype="pdf") as document:
        text = "\n".join(page.get_text("text") for page in document).strip()
        return ParsedDocument(text=text, page_count=len(document), file_type="pdf")


def _parse_docx(data: bytes) -> ParsedDocument:
    document = Document(BytesIO(data))
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs]
    table_cells = [
        cell.text.strip()
        for table in document.tables
        for row in table.rows
        for cell in row.cells
    ]
    text = "\n".join(part for part in paragraphs + table_cells if part)
    return ParsedDocument(text=text, page_count=None, file_type="docx")

