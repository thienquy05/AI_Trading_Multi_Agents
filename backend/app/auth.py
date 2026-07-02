"""JWT issuing/verification and the single auth gate (scaffold-roadmap §2).

No roles: `get_current_operator` is the one dependency that guards every
mutating endpoint built after this branch.
"""
import uuid
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models.user import User

ALGORITHM = "HS256"

# auto_error=False so a missing header raises our uniform 401 below
# instead of HTTPBearer's 403.
_bearer = HTTPBearer(auto_error=False)


def _secret() -> str:
    secret = get_settings().jwt_secret_key
    if not secret:
        raise RuntimeError(
            "JWT_SECRET_KEY is not set. Generate one with "
            '`python -c "import secrets; print(secrets.token_urlsafe(48))"` '
            "and put it in .env before serving authenticated endpoints."
        )
    return secret


def create_access_token(user: User) -> tuple[str, int]:
    """Returns (token, expires_in_seconds)."""
    settings = get_settings()
    ttl = timedelta(minutes=settings.jwt_ttl_minutes)
    now = datetime.now(timezone.utc)
    claims = {"sub": str(user.id), "iat": now, "exp": now + ttl}
    return jwt.encode(claims, _secret(), algorithm=ALGORITHM), int(ttl.total_seconds())


def _unauthorized() -> HTTPException:
    # One message for every failure mode — the response never reveals
    # whether the token was absent, expired, forged, or for a gone user.
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_operator(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise _unauthorized()
    try:
        claims = jwt.decode(
            credentials.credentials,
            _secret(),
            algorithms=[ALGORITHM],
            options={"require": ["sub", "exp"]},
        )
        user_id = uuid.UUID(claims["sub"])
    except (jwt.InvalidTokenError, ValueError):
        raise _unauthorized() from None

    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise _unauthorized()
    return user
