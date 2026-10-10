
import pymupdf
import pytest

from backend.app.ingestion import (
    chunk_text,
    extract_pdf_pages,
    ingest_pdf,
)


def test_chunk_text_preserves_document_metadata():
    chunks = chunk_text(
        text="Hello world",
        document_id="doc-001",
        department="HR",
        chunk_size=50,
        overlap=5,
    )

    assert len(chunks) == 1
    assert chunks[0].document_id == "doc-001"
    assert chunks[0].department == "hr"
    assert chunks[0].text == "Hello world"
    assert chunks[0].page_number is None


def test_empty_text_returns_no_chunks():
    assert chunk_text("", "doc-001", "hr") == []
    assert chunk_text("   ", "doc-001", "hr") == []


def test_invalid_chunk_size_is_rejected():
    with pytest.raises(ValueError, match="chunk_size"):
        chunk_text("Hello", "doc-001", "hr", chunk_size=0)


def test_invalid_overlap_is_rejected():
    with pytest.raises(ValueError, match="overlap"):
        chunk_text("Hello", "doc-001", "hr", chunk_size=10, overlap=10)


def test_empty_document_id_is_rejected():
    with pytest.raises(ValueError, match="document_id"):
        chunk_text("Hello", "   ", "hr")


def test_extract_pdf_pages_preserves_text_and_page_numbers(tmp_path):
    pdf_path = tmp_path / "sample.pdf"

    with pymupdf.open() as pdf:
        first_page = pdf.new_page()
        first_page.insert_text((72, 72), "HR onboarding policy")

        second_page = pdf.new_page()
        second_page.insert_text((72, 72), "Employee benefits guide")

        pdf.save(str(pdf_path))

    pages = extract_pdf_pages(str(pdf_path))

    assert len(pages) == 2
    assert pages[0]["page_number"] == 1
    assert "HR onboarding policy" in pages[0]["text"]
    assert pages[1]["page_number"] == 2
    assert "Employee benefits guide" in pages[1]["text"]


def test_extract_pdf_pages_handles_empty_page(tmp_path):
    pdf_path = tmp_path / "empty.pdf"

    with pymupdf.open() as pdf:
        pdf.new_page()
        pdf.save(str(pdf_path))

    pages = extract_pdf_pages(str(pdf_path))

    assert len(pages) == 1
    assert pages[0]["page_number"] == 1
    assert pages[0]["text"] == ""


def test_ingest_pdf_preserves_page_numbers(tmp_path):
    pdf_path = tmp_path / "sample.pdf"

    with pymupdf.open() as pdf:
        first_page = pdf.new_page()
        first_page.insert_text((72, 72), "HR onboarding policy")

        second_page = pdf.new_page()
        second_page.insert_text((72, 72), "Employee benefits guide")

        pdf.save(str(pdf_path))

    chunks = ingest_pdf(
        pdf_path=str(pdf_path),
        document_id="hr-policy",
        department="hr",
    )

    assert len(chunks) == 2
    assert chunks[0].document_id == "hr-policy"
    assert chunks[0].department == "hr"
    assert chunks[0].page_number == 1
    assert "HR onboarding policy" in chunks[0].text
    assert chunks[1].page_number == 2
    assert "Employee benefits guide" in chunks[1].text
