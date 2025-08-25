import os
import pytest
from src.models.services.shop_service import ShopService

@pytest.fixture
def shop_service():
    return ShopService()

@pytest.mark.smoke
def test_delete_shop_success(client):
    payload = {"address": "123 Delete St", "manager": "Dan"}
    shop = client.post("/shops", json=payload).json()
    shop_id = shop["id"]

    response = client.delete(f"/shops/{shop_id}")

    assert response.status_code == 204
    response_check = client.get(f"/shops/{shop_id}")
    assert response_check.status_code == 404
