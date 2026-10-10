from dataclasses import dataclass

from backend.app.auth import User


@dataclass(frozen=True)
class Document:
    """A document with an access-control label."""

    document_id: str
    department: str
    content: str


# Temporary sample documents for testing authorization.
SAMPLE_DOCUMENTS: list[Document] = [
    Document(
        document_id="hr-001",
        department="hr",
        content="HR employee onboarding policy.",
    ),
    Document(
        document_id="finance-001",
        department="finance",
        content="Finance annual budget report.",
    ),
]


def can_access_document(user: User, document: Document) -> bool:
    """Return whether a user is allowed to access a document."""
    if user.role == "admin":
        return True

    return user.role == document.department


def retrieve_documents(user: User) -> list[Document]:
    """Return only documents the user is authorized to access."""
    return [
        document
        for document in SAMPLE_DOCUMENTS
        if can_access_document(user, document)
    ]
