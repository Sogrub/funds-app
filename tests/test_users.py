import pytest

@pytest.fixture(scope="module")
def created_user_id(test_client):
    response = test_client.post("/users", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password"
    })
    data = response.json()
    return data["data"]["id"]

def test_create_user(test_client):
    payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password"
    }

    response = test_client.post("/users/", json=payload)
    assert response.status_code == 201 or response.status_code == 200
    data = response.json()
    assert data["data"]["name"] == "John Doe"
    assert data["data"]["email"] == "john@example.com"


def test_list_users(test_client):
    test_client.post("/users/", json={
        "id": 2,
        "name": "Jane Doe",
        "email": "jane@example.com",
        "balance": 1500
    })

    response = test_client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    users = data["data"]
    assert isinstance(users, list)


def test_update_balance(test_client, created_user_id):
    response = test_client.put(f"/users/{created_user_id}/balance", params={"balance": 2000})
    assert response.status_code == 200
    data = response.json()
    updated_user = data["data"]
    assert updated_user["balance"] == 2000
