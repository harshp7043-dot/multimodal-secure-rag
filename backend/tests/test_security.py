from backend.app.auth import User
from backend.app.retrieval import retrieve_documents


def test_hr_user_only_retrieves_hr_documents():
    user = User(user_id="hr-user", role="hr")

    documents = retrieve_documents(user)

    assert len(documents) == 1
    assert documents[0].document_id == "hr-001"


def test_finance_user_only_retrieves_finance_documents():
    user = User(user_id="finance-user", role="finance")

    documents = retrieve_documents(user)

    assert len(documents) == 1
    assert documents[0].document_id == "finance-001"


def test_admin_can_retrieve_all_documents():
    user = User(user_id="admin-user", role="admin")

    documents = retrieve_documents(user)

    document_ids = {document.document_id for document in documents}

    assert document_ids == {"hr-001", "finance-001"}


def test_unknown_role_cannot_retrieve_documents():
    user = User(user_id="guest-user", role="guest")

    documents = retrieve_documents(user)

    assert documents == []
