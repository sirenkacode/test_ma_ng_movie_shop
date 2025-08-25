import os
import pytest
from src.models.services.shop_service import ShopService

@pytest.fixture
def shop_service():
    return ShopService()

@pytest.mark.smoke
def test_update_shop_success(client):
    payload = {"address": "456 Market St", "manager": "Bob"}
    shop = client.post("/shops", json=payload).json()
    shop_id = shop["id"]

    update_payload = {"address": "789 Updated St", "manager": "Charlie"}

    response = client.put(f"/shops/{shop_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["address"] == "789 Updated St"
    assert data["manager"] == "Charlie"
