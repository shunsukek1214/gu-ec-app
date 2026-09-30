#google ID tokenを検証する処理

from google.oauth2 import id_token
from google.auth.transport.requests import Request

from app.core.config import settings

def verify_google_id_token(token: str):
    payload = id_token.verify_oauth2_token(
        token,
        Request(),
        settings.google_client_id,  #GUアプリ向けに発行されたトークンか検証
    )

    return {
        "google_sub": payload["sub"],
        "email": payload["email"],
        "name": payload["name"],
    }