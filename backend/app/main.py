
from fastapi import FastAPI

app = FastAPI(
    title="Secure Multimodal RAG",
    description="A secure retrieval-augmented generation API",
    version="0.1.0",
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Return the health status of the API."""
    return {
        "status": "healthy",
        "service": "secure-multimodal-rag",
    }


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    """Return basic API information."""
    return {
        "message": "Secure Multimodal RAG API",
        "docs": "/docs",
    }
