import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app import app

client = TestClient(app)

@patch("app.http_request")
def test_read_orders_valid_customer_id(mock_http_request):
    # Mock the http_request function to return a specific response
    mock_response = MagicMock()
    mock_response.json.return_value = {"orders": ["order1", "order2"]}
    mock_http_request.return_value = mock_response

    # Perform the test
    response = client.get("/orders/7480919556431")

    # Assertions
    assert response.status_code == 200
    assert "orders" in response.json()
    assert len(response.json()["orders"]) > 0

@patch("app.http_request")
def test_read_orders_invalid_customer_id(mock_http_request):
    # Mock the http_request function to raise an exception, simulating a failure
    mock_http_request.side_effect = Exception("HTTP request failed")

    # Perform the test
    response = client.get("/orders/99999")

    # Assertions
    assert response.status_code == 500
    assert "detail" in response.json()
    assert response.json()["detail"] == "Failed to fetch orders: HTTP request failed"
