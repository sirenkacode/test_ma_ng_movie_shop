import pytest
from src.models.services.shop_service import ShopService

@pytest.fixture
def shop_service():
    return ShopService()

@pytest.mark.smoke
def test_create_shop_success(shop_service):
    """
    TC-007 — POST /shops success
    Crea un shop y valida campos básicos de respuesta.
    """
    payload = {"address": "Cinema Plaza", "manager": "Grace"}

    resp = shop_service.add_shop(shop=payload, response_type=None)
    assert resp.status in (200, 201)

    data = resp.data
    assert isinstance(data, dict)
    for k in ("id", "address", "manager"):
        assert k in data

    assert isinstance(data["id"], int)
    assert data["address"] == "Cinema Plaza"
    assert data["manager"] == "Grace"
