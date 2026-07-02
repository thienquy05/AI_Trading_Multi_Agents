"""Login gate (scaffold-roadmap §2). No registration endpoint on purpose —
the operator is seeded by `python -m app.cli seed-operator`.
"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from redis import Redis
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_operator
from app.config import get_settings
from app.database import get_db
from app.models.user import User
from app.redis_client import get_redis
from app.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

# Constant-cost verify target for unknown usernames — keeps the response
# time of "no such user" indistinguishable from "wrong password".
_DUMMY_HASH = hash_password("timing-equalizer")


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class OperatorResponse(BaseModel):
    id: str
    username: str
    last_login_at: datetime | None


def _failure_key(username: str) -> str:
    return f"login:failures:{username}"


def _too_many_attempts(retry_after: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail="Too many failed login attempts. Try again later.",
        headers={"Retry-After": str(retry_after)},
    )


@router.post("/login", response_model=TokenResponse)
def login(
    body: LoginRequest,
    db: Session = Depends(get_db),
    redis_conn: Redis = Depends(get_redis),
) -> TokenResponse:
    settings = get_settings()
    key = _failure_key(body.username)

    failures = redis_conn.get(key)
    if failures is not None and int(failures) >= settings.login_max_failures:
        ttl = redis_conn.ttl(key)
        raise _too_many_attempts(max(ttl, 1))

    user = db.execute(select(User).where(User.username == body.username)).scalar_one_or_none()
    password_ok = verify_password(body.password, user.password_hash if user else _DUMMY_HASH)

    if user is None or not user.is_active or not password_ok:
        # Count the failure inside the fixed window, then answer with one
        # uniform message — never reveal which check failed.
        if redis_conn.incr(key) == 1:
            redis_conn.expire(key, settings.login_failure_window_seconds)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    redis_conn.delete(key)
    user.last_login_at = datetime.now(timezone.utc)
    db.commit()

    token, expires_in = create_access_token(user)
    return TokenResponse(access_token=token, expires_in=expires_in)


@router.get("/me", response_model=OperatorResponse)
def me(operator: User = Depends(get_current_operator)) -> OperatorResponse:
    """First consumer of the auth gate — also the smoke check for it."""
    return OperatorResponse(
        id=str(operator.id),
        username=operator.username,
        last_login_at=operator.last_login_at,
    )
