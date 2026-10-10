
import chromadb

from backend.app.ingestion import DocumentChunk


class VectorStore:
    """Store and retrieve document chunks using ChromaDB."""

    def __init__(
        self,
        collection_name: str = "secure_documents",
        persist_directory: str = "data/chroma",
    ):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
        )

    def add_chunks(self, chunks: list[DocumentChunk]) -> None:
        """Add document chunks and their access-control metadata."""
        if not chunks:
            return

        self.collection.upsert(
            ids=[chunk.chunk_id for chunk in chunks],
            documents=[chunk.text for chunk in chunks],
            metadatas=[
                {
                    "document_id": chunk.document_id,
                    "department": chunk.department,
                    "page_number": chunk.page_number or 0,
                }
                for chunk in chunks
            ],
        )

    def search(
        self,
        query: str,
        department: str,
        n_results: int = 5,
    ) -> list[dict]:
        """Search chunks restricted to a specific department."""
        if not query.strip():
            return []

        if not department.strip():
            return []

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"department": department.strip().lower()},
        )

        matches = []
        for index, text in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][index]
            matches.append(
                {
                    "text": text,
                    "document_id": metadata["document_id"],
                    "department": metadata["department"],
                    "page_number": metadata["page_number"],
                }
            )

        return matches
