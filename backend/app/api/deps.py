#FastAPIの複数APIで共通して使用するDependency
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError

from app.core.security import decode_access_token
from app.core.security import (
    decode_access_token,
    decode_registration_token,
)

bearer_scheme = HTTPBearer(auto_error=False)

#Bearer Tokenを検証し、ユーザーIDを取得する
def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> int:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = decode_access_token(credentials.credentials)
        return user_id
    except (InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    

def get_registration_payload(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Registration token is required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_registration_token(
            credentials.credentials
        )

        return payload

    except (InvalidTokenError, ValueError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired registration token",
            headers={"WWW-Authenticate": "Bearer"},
        )