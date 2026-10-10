from dataclasses import dataclass

from fastapi import Header, HTTPException, status


@dataclass(frozen=True)
class User:
    """Represents an authenticated user."""

    user_id: str
    role: str


# Development-only API keys. Do not use these in production.
API_KEYS: dict[str, User] = {
    "dev-hr-key": User(user_id="hr-user", role="hr"),
    "dev-finance-key": User(user_id="finance-user", role="finance"),
    "dev-admin-key": User(user_id="admin-user", role="admin"),
}


def get_current_user(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> User:
    """Authenticate a request using its X-API-Key header."""
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )

    user = API_KEYS.get(x_api_key)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return user
