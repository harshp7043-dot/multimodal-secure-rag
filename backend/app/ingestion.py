from dataclasses import dataclass



@dataclass(frozen=True)
class DocumentChunk:
    """A text chunk with its source and access-control metadata."""

    chunk_id: str
    document_id: str
    department: str
    text: str
    page_number: int | None = None


def chunk_text(
    text: str,
    document_id: str,
    department: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[DocumentChunk]:
    """Split text into overlapping chunks with document metadata."""
    if not document_id.strip():
        raise ValueError("document_id must not be empty")

    if not department.strip():
        raise ValueError("department must not be empty")

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size")

    cleaned_text = " ".join(text.split())

    if not cleaned_text:
        return []

    chunks: list[DocumentChunk] = []
    start = 0

    while start < len(cleaned_text):
        end = min(start + chunk_size, len(cleaned_text))
        chunk_number = len(chunks) + 1

        chunks.append(
            DocumentChunk(
                chunk_id=f"{document_id}-chunk-{chunk_number}",
                document_id=document_id,
                department=department.strip().lower(),
                text=cleaned_text[start:end],
                
            )
        )

        if end == len(cleaned_text):
            break

        start = end - overlap

    return chunks
import pymupdf


def extract_pdf_pages(pdf_path: str) -> list[dict[str, str | int]]:
    """Extract text from each PDF page, preserving page numbers."""
    pages: list[dict[str, str | int]] = []

    with pymupdf.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            pages.append(
                {
                    "page_number": page_number,
                    "text": page.get_text().strip(),
                }
            )

    return pages

def ingest_pdf(
    pdf_path: str,
    document_id: str,
    department: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[DocumentChunk]:
    """Extract a PDF and split its pages into chunks with source metadata."""
    pages = extract_pdf_pages(pdf_path)
    all_chunks: list[DocumentChunk] = []

    for page in pages:
        page_number = int(page["page_number"])
        page_text = str(page["text"])

        page_chunks = chunk_text(
            text=page_text,
            document_id=f"{document_id}-page-{page_number}",
            department=department,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for chunk in page_chunks:
            all_chunks.append(
                DocumentChunk(
                    chunk_id=chunk.chunk_id,
                    document_id=document_id,
                    department=chunk.department,
                    text=chunk.text,
                    page_number=page_number,
                )
            )

    return all_chunks

