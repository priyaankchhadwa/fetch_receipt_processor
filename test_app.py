from app import app, parse_receipt, calculate_points
import pytest
from uuid import uuid4


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client

ids = {}

def test_parse_receipt_valid(client):
    data = {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
            {
                "shortDescription": "Gatorade",
                "price": "2.25"
            },{
                "shortDescription": "Gatorade",
                "price": "2.25"
            },{
                "shortDescription": "Gatorade",
                "price": "2.25"
            },{
                "shortDescription": "Gatorade",
                "price": "2.25"
            }
        ],
        "total": "9.00"
    }
    
    response = client.post("/receipts/process", json=data)
    ids["receipt_id"] = response.json["id"]

    assert response.status_code == 200
    assert "id" in response.json


def test_calculate_points_valid(client):
    points_res = client.get(f"/receipts/{ids['receipt_id']}/points")

    assert points_res.json["points"] == 109


def test_parse_receipt_invalid(client):
    data = {
        "retailer": "Walgreens",
        "purchaseDate": "2022-01-02",
        "purchasTime": "08:13",             # Typo in purchaseTime
        "total": "2.65",
        "items": [
            {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
            {"shortDescription": "Dasani", "price": "1.40"}
        ]
    }

    response = client.post("/receipts/process", json=data)

    assert response.status_code == 400

def test_calculate_points_invalid(client):
    points_res = client.get(f"/receipts/some-random-id/points")

    assert points_res.status_code == 404