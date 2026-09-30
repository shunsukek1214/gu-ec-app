from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from jwt.exceptions import InvalidTokenError

from app.core.config import settings

#JWTを作る関数
def create_access_token(
        user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    now = datetime.now(timezone.utc)
    expires_delta = expires_delta or timedelta(minutes=settings.jwt_access_token_expire_minutes) #有効期限を計算
    expire = now + expires_delta

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": expire,
        "purpose": "api_access"
    }

    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

#JWTからuser_idを取得する関数
def decode_access_token(token: str) -> int:
    
    payload = jwt.decode(
        token, 
        settings.jwt_secret_key, 
        algorithms=[settings.jwt_algorithm],
        options={"require": ["sub", "exp", "iat"]},  # 必須クレームを指定)
    )
    if payload.get("purpose") != "api_access":
        raise InvalidTokenError("Invalid token purpose")

    user_id = int(payload["sub"])

    return user_id

#登録用トークンを作る関数
def create_registration_token(
        google_sub: str,
        email: str,
        name: str,
) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": google_sub,
        "email": email,
        "name": name,
        "purpose": "registration",
        "iat": now,
        "exp": now + timedelta(minutes=15),
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

#登録用トークンを検証・解析する関数
def decode_registration_token(token: str) -> dict:
    payload = jwt.decode(
        token, 
        settings.jwt_secret_key, 
        algorithms=[settings.jwt_algorithm],
        options={"require": ["sub", "email", "name", "exp", "iat", "purpose",]},  # 必須クレームを指定)
    )

    if payload.get("purpose") != "registration":
        raise InvalidTokenError("Invalid token purpose")

    return payload