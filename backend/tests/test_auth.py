"""Auth flow tests (scaffold-roadmap §2 verification gate): wrong password,
expired token, missing token, rate-limit trip — plus the seeder CLI.

Needs live Postgres (conftest fixtures) for user rows; Redis is faked so
the rate limiter runs deterministically without a server.
"""
import uuid
from datetime import datetime, timedelta, timezone

import fakeredis
import jwt as pyjwt
import pytest
from fastapi.testclient import TestClient

from app import cli
from app.auth import ALGORITHM, create_access_token
from app.config import get_settings
from app.database import get_db
from app.main import app
from app.models.user import User
from app.redis_client import get_redis
from app.security import hash_password, verify_password

PASSWORD = "correct-horse-battery"


@pytest.fixture(autouse=True)
def jwt_secret(monkeypatch, clear_settings_cache):
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret")


@pytest.fixture()
def fake_redis():
    return fakeredis.FakeRedis(decode_responses=True)


@pytest.fixture()
def client(db_session, fake_redis):
    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_redis] = lambda: fake_redis
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


@pytest.fixture()
def operator(db_session):
    user = User(username="operator", password_hash=hash_password(PASSWORD))
    db_session.add(user)
    db_session.flush()
    return user


def login(client, username="operator", password=PASSWORD):
    return client.post("/auth/login", json={"username": username, "password": password})


def auth_header(response) -> dict:
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


# --- login -----------------------------------------------------------------


def test_login_success_returns_bearer_token(client, operator):
    response = login(client)
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == get_settings().jwt_ttl_minutes * 60
    assert body["access_token"]


def test_login_updates_last_login_at(client, operator):
    assert operator.last_login_at is None
    login(client)
    assert operator.last_login_at is not None


def test_login_wrong_password_is_401(client, operator):
    response = login(client, password="wrong-password")
    assert response.status_code == 401


def test_login_unknown_user_is_401_with_same_body_as_wrong_password(client, operator):
    unknown = login(client, username="nobody")
    wrong = login(client, password="wrong-password")
    assert unknown.status_code == wrong.status_code == 401
    assert unknown.json() == wrong.json()  # no user-enumeration oracle


def test_login_inactive_user_is_401(client, db_session, operator):
    operator.is_active = False
    db_session.flush()
    assert login(client).status_code == 401


# --- rate limiting ----------------------------------------------------------


def test_rate_limit_trips_after_max_failures(client, operator):
    limit = get_settings().login_max_failures
    for _ in range(limit):
        assert login(client, password="wrong-password").status_code == 401

    limited = login(client, password="wrong-password")
    assert limited.status_code == 429
    assert int(limited.headers["Retry-After"]) >= 1


def test_rate_limit_blocks_even_the_correct_password(client, operator):
    for _ in range(get_settings().login_max_failures):
        login(client, password="wrong-password")
    assert login(client).status_code == 429


def test_successful_login_clears_the_failure_counter(client, operator):
    for _ in range(get_settings().login_max_failures - 1):
        login(client, password="wrong-password")
    assert login(client).status_code == 200
    # counter reset: a fresh string of failures is tolerated again
    assert login(client, password="wrong-password").status_code == 401


def test_rate_limit_window_expires(client, operator, fake_redis):
    for _ in range(get_settings().login_max_failures):
        login(client, password="wrong-password")
    assert login(client).status_code == 429

    fake_redis.delete("login:failures:operator")  # window elapsed
    assert login(client).status_code == 200


# --- token verification (/auth/me as the gate's first consumer) -------------


def test_me_with_valid_token(client, operator):
    response = client.get("/auth/me", headers=auth_header(login(client)))
    assert response.status_code == 200
    body = response.json()
    assert body["username"] == "operator"
    assert body["id"] == str(operator.id)


def test_me_missing_token_is_401(client, operator):
    response = client.get("/auth/me")
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_me_garbage_token_is_401(client, operator):
    response = client.get("/auth/me", headers={"Authorization": "Bearer not.a.jwt"})
    assert response.status_code == 401


def test_me_expired_token_is_401(client, operator):
    past = datetime.now(timezone.utc) - timedelta(minutes=5)
    expired = pyjwt.encode(
        {"sub": str(operator.id), "iat": past - timedelta(minutes=30), "exp": past},
        get_settings().jwt_secret_key,
        algorithm=ALGORITHM,
    )
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {expired}"})
    assert response.status_code == 401


def test_me_token_signed_with_wrong_secret_is_401(client, operator):
    forged = pyjwt.encode(
        {"sub": str(operator.id), "exp": datetime.now(timezone.utc) + timedelta(minutes=5)},
        "not-the-real-secret",
        algorithm=ALGORITHM,
    )
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {forged}"})
    assert response.status_code == 401


def test_me_token_for_deleted_user_is_401(client, db_session, operator):
    token, _ = create_access_token(operator)
    db_session.delete(operator)
    db_session.flush()
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_me_token_for_deactivated_user_is_401(client, db_session, operator):
    header = auth_header(login(client))
    operator.is_active = False
    db_session.flush()
    assert client.get("/auth/me", headers=header).status_code == 401


def test_token_creation_refuses_to_run_without_secret(monkeypatch, clear_settings_cache):
    monkeypatch.setenv("JWT_SECRET_KEY", "")
    get_settings.cache_clear()
    user = User(id=uuid.uuid4(), username="x", password_hash="h")
    with pytest.raises(RuntimeError, match="JWT_SECRET_KEY"):
        create_access_token(user)


# --- CORS pin ----------------------------------------------------------------


def test_cors_allows_only_the_frontend_origin(client):
    allowed = get_settings().frontend_origin
    ok = client.options(
        "/auth/login",
        headers={"Origin": allowed, "Access-Control-Request-Method": "POST"},
    )
    assert ok.headers.get("access-control-allow-origin") == allowed

    denied = client.options(
        "/auth/login",
        headers={"Origin": "https://evil.example", "Access-Control-Request-Method": "POST"},
    )
    assert "access-control-allow-origin" not in denied.headers


# --- seeder CLI ---------------------------------------------------------------


@pytest.fixture()
def seeder_env(monkeypatch, db_session):
    # Point the CLI's SessionLocal at the test transaction so its commit()
    # stays inside the outer rollback.
    monkeypatch.setattr(cli, "SessionLocal", lambda: db_session)
    monkeypatch.setattr(db_session, "close", lambda: None)  # context-manager exit
    monkeypatch.setattr(db_session, "commit", db_session.flush)
    monkeypatch.setenv("OPERATOR_USERNAME", "seeded_op")
    monkeypatch.setenv("OPERATOR_PASSWORD", "a-long-enough-password")


def test_seed_operator_creates_user(seeder_env, db_session):
    cli.main(["seed-operator"])
    user = db_session.query(User).filter_by(username="seeded_op").one()
    assert verify_password("a-long-enough-password", user.password_hash)
    assert user.is_active


def test_seed_operator_refuses_duplicate(seeder_env, db_session):
    cli.main(["seed-operator"])
    with pytest.raises(SystemExit, match="already exists"):
        cli.main(["seed-operator"])


def test_seed_operator_reset_password(seeder_env, monkeypatch, db_session):
    cli.main(["seed-operator"])
    monkeypatch.setenv("OPERATOR_PASSWORD", "another-long-password")
    cli.main(["seed-operator", "--reset-password"])
    user = db_session.query(User).filter_by(username="seeded_op").one()
    assert verify_password("another-long-password", user.password_hash)


def test_seed_operator_rejects_short_password(seeder_env, monkeypatch):
    monkeypatch.setenv("OPERATOR_PASSWORD", "short")
    with pytest.raises(SystemExit, match="at least"):
        cli.main(["seed-operator"])
