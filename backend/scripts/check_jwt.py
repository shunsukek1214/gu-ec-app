from app.core.security import (
    create_access_token,
    decode_access_token,
)

token = create_access_token(user_id=1)
print(f"Generated JWT: {token}")

user_id = decode_access_token(token)
print(f"Decoded User ID: {user_id}")