
from backend.app.ingestion import DocumentChunk
from backend.app.vector_store import VectorStore


def test_search_returns_only_matching_department(tmp_path):
    store = VectorStore(
    collection_name="test_department_isolation",
    persist_directory=str(tmp_path / "chroma"),
)

    store.add_chunks(
        [
            DocumentChunk(
                chunk_id="hr-001",
                document_id="hr-policy",
                department="hr",
                text="Employee onboarding and recruitment policy",
            ),
            DocumentChunk(
                chunk_id="finance-001",
                document_id="finance-report",
                department="finance",
                text="Annual budget and financial reporting",
            ),
        ]
    )

    results = store.search(
        query="employee onboarding",
        department="hr",
    )

    assert len(results) == 1
    assert results[0]["department"] == "hr"
    assert results[0]["document_id"] == "hr-policy"


def test_search_returns_no_results_for_other_department(tmp_path):
    store = VectorStore(
    collection_name="test_empty_department",
    persist_directory=str(tmp_path / "chroma"),
)

    store.add_chunks(
        [
            DocumentChunk(
                chunk_id="hr-002",
                document_id="hr-policy",
                department="hr",
                text="Employee onboarding policy",
            ),
        ]
    )

    results = store.search(
        query="employee onboarding",
        department="finance",
    )

    assert results == []


def test_search_empty_query_returns_no_results():
    store = VectorStore(collection_name="test_empty_query")

    results = store.search(query="   ", department="hr")

    assert results == []
