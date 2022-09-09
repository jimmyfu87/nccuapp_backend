from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_read_user_me():
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json() == {"username":"fakecurrentuser"}