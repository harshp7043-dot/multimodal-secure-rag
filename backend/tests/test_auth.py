from fastapi import HTTPException

from backend.app.auth import get_current_user


def test_valid_hr_api_key():
    user = get_current_user(x_api_key="dev-hr-key")

    assert user.user_id == "hr-user"
    assert user.role == "hr"


def test_valid_admin_api_key():
    user = get_current_user(x_api_key="dev-admin-key")

    assert user.user_id == "admin-user"
    assert user.role == "admin"


def test_missing_api_key():
    try:
        get_current_user(x_api_key=None)
        assert False, "Expected missing API key to be rejected"
    except HTTPException as exc:
        assert exc.status_code == 401
        assert exc.detail == "Missing API key"


def test_invalid_api_key():
    try:
        get_current_user(x_api_key="wrong-key")
        assert False, "Expected invalid API key to be rejected"
    except HTTPException as exc:
        assert exc.status_code == 401
        assert exc.detail == "Invalid API key"