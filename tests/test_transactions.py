def test_list_transactions(test_client):
    response = test_client.get("/transactions/")
    assert response.status_code == 200
    data = response.json()
    transactions = data["data"]
    assert isinstance(transactions, list)