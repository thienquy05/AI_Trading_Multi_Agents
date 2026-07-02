"""Operational commands. Usage: python -m app.cli seed-operator [--reset-password]

`seed-operator` creates the single operator login (scaffold-roadmap §2:
no open registration — this command is the only way a user row is born).
Credentials come from OPERATOR_USERNAME / OPERATOR_PASSWORD, falling back
to an interactive prompt.
"""
import argparse
import getpass
import os
import sys

from sqlalchemy import select

from app.database import SessionLocal
from app.models.user import User
from app.security import hash_password

MIN_PASSWORD_LENGTH = 12


def _read_credentials() -> tuple[str, str]:
    username = os.environ.get("OPERATOR_USERNAME") or input("Operator username: ").strip()
    password = os.environ.get("OPERATOR_PASSWORD") or getpass.getpass("Operator password: ")
    if not username:
        sys.exit("error: username is empty")
    if len(password) < MIN_PASSWORD_LENGTH:
        sys.exit(f"error: password must be at least {MIN_PASSWORD_LENGTH} characters")
    return username, password


def seed_operator(reset_password: bool = False) -> None:
    username, password = _read_credentials()
    with SessionLocal() as db:
        existing = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
        if existing is not None:
            if not reset_password:
                sys.exit(
                    f"error: user {username!r} already exists "
                    "(use --reset-password to set a new password)"
                )
            existing.password_hash = hash_password(password)
            existing.is_active = True
            db.commit()
            print(f"password reset for operator {username!r}")
            return
        db.add(User(username=username, password_hash=hash_password(password)))
        db.commit()
        print(f"operator {username!r} created")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="python -m app.cli")
    sub = parser.add_subparsers(dest="command", required=True)
    seed = sub.add_parser("seed-operator", help="create (or re-key) the operator login")
    seed.add_argument(
        "--reset-password",
        action="store_true",
        help="if the user already exists, replace its password and reactivate it",
    )
    args = parser.parse_args(argv)

    if args.command == "seed-operator":
        seed_operator(reset_password=args.reset_password)


if __name__ == "__main__":
    main()
