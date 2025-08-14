def test_create_fund(test_client):
    payload = {
        "name": "Green Energy Fund",
        "category": "FPV",
        "min_amount": 500000
    }

    response = test_client.post("/funds/", json=payload)
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["data"]["name"] == "Green Energy Fund"
    assert data["data"]["category"] == "FPV"
    assert data["data"]["min_amount"] == 500000

def test_list_funds(test_client):
    response = test_client.get("/funds/")
    assert response.status_code == 200
    data = response.json()
    funds = data["data"]
    assert isinstance(funds, list)