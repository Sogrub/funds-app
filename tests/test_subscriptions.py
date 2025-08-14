import pytest

@pytest.fixture(scope="module")
def created_user_id(test_client):
    response = test_client.post("/users", json={
        "name": "Test User 2",
        "email": "test2@example.com",
        "password": "password"
    })
    data = response.json()
    return data["data"]["id"]

@pytest.fixture(scope="module")
def created_fund_id(test_client):
    response = test_client.post("/funds", json={
        "name": "Test Fund 2",
        "category": "FPV",
        "min_amount": 1000
    })
    data = response.json()
    return data["data"]["id"]

@pytest.fixture(scope="module")
def created_fund_id2(test_client):
    response = test_client.post("/funds", json={
        "name": "Test Fund 3",
        "category": "FPV",
        "min_amount": 1000
    })
    data = response.json()
    return data["data"]["id"]


@pytest.fixture(scope="module")
def created_subscription_id(test_client, created_user_id, created_fund_id):
    payload = {
        "user_id": created_user_id,
        "fund_id": created_fund_id,
        "amount": 1000
    }
    response = test_client.post("/subscriptions/", json=payload)
    assert response.status_code in (200, 201)
    data = response.json()
    return data["data"]["id"]


def test_create_subscription(test_client, created_user_id, created_fund_id2):
    payload = {
        "user_id": created_user_id,
        "fund_id": created_fund_id2,
        "amount": 5000
    }
    response = test_client.post("/subscriptions/", json=payload)
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["data"]["user_id"] == created_user_id
    assert data["data"]["fund_id"] == created_fund_id2
    assert data["data"]["amount"] == 5000


def test_list_subscriptions(test_client):
    response = test_client.get("/subscriptions/")
    assert response.status_code == 200
    data = response.json()
    subs = data["data"]
    assert isinstance(subs, list)


def test_update_subscription(test_client, created_subscription_id):
    print("created_subscription_id", created_subscription_id)
    response = test_client.patch(
        f"/subscriptions/{created_subscription_id}",
        params={"type": "CANCELLED"}
    )
    assert response.status_code == 200
    data = response.json()
    updated = data["data"]
    assert updated["type"] == "CANCELLED"
