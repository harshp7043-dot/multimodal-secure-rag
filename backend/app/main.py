from fastapi import Depends, FastAPI, HTTPException, Query

from backend.app.auth import User, get_current_user
from backend.app.vector_store import VectorStore

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


@app.get("/search", tags=["Search"])
def search_documents(
    query: str = Query(..., min_length=1),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Search documents available to the authenticated user."""
    if current_user.role == "admin":
        raise HTTPException(
            status_code=400,
            detail="Admin cross-department search is not supported yet",
        )

    store = VectorStore()
    results = store.search(
        query=query,
        department=current_user.role,
    )

    return {"results": results}