from app.core.security import create_access_token, decode_access_token

def test_create_and_decode_access_token():

    # Create a token for user_id 123
    token = create_access_token(user_id=123)
    assert token is not None, "Failed to create access token"

    # Decode the token and verify the user_id
    user_id = decode_access_token(token)
    assert user_id == 123, "Decoded user_id does not match"