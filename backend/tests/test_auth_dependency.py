from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from app.api.deps import get_current_user_id
from app.core.security import create_access_token

app = FastAPI()

@app.get("/protected")
def protected(user_id: int = Depends(get_current_user_id)):
    return {"user_id": user_id}

client = TestClient(app)

def test_get_current_user_id():
    token = create_access_token(user_id=123)

    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == {"user_id": 123}