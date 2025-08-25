import os
import pytest
from src.models.services.shop_service import ShopService

@pytest.fixture
def shop_service():
    return ShopService()

@pytest.mark.smoke
def test_create_shop_success(client):
    payload = {"address": "123 Main St", "manager": "Alice"}
    
    response = client.post("/shops", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["address"] == "123 Main St"
    assert data["manager"] == "Alice"
    assert "id" in data
