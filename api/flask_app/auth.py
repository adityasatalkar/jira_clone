import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Dict

import jwt
from flask import g, request

from .errors import InvalidTokenError
from .models import User


JWT_ALGORITHM = "HS256"


def sign_token(payload: Dict, expires_in_days: int = 180) -> str:
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET must be set")

    now = datetime.now(timezone.utc)
    complete_payload = {
        **payload,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=expires_in_days)).timestamp()),
    }
    return jwt.encode(complete_payload, secret, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> Dict:
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET must be set")

    try:
        payload = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
        if isinstance(payload, dict):
            return payload
        raise InvalidTokenError()
    except jwt.InvalidTokenError as exc:
        raise InvalidTokenError() from exc


def _get_auth_token_from_request() -> str | None:
    header = request.headers.get("Authorization", "")
    bearer, _, token = header.partition(" ")
    if bearer == "Bearer" and token:
        return token
    return None


def require_auth(handler):
    @wraps(handler)
    def wrapped(*args, **kwargs):
        token = _get_auth_token_from_request()
        if not token:
            raise InvalidTokenError("Authentication token not found.")

        payload = verify_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise InvalidTokenError("Authentication token is invalid.")

        user = User.query.get(user_id)
        if not user:
            raise InvalidTokenError("Authentication token is invalid: User not found.")

        g.current_user = user
        return handler(*args, **kwargs)

    return wrapped
