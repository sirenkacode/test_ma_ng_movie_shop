import pytest
from src.models.services.shop_service import ShopService

@pytest.fixture
def shop_service():
    return ShopService()

def test_update_shop_success(shop_service):
    """
    PUT/PATCH /shops/{id} success (solo si tu SDK expone update_shop).
    Si no existe update_shop en ShopService, se marca skipped.
    """
    # Crear base
    created = shop_service.add_shop({"address": "Old Addr", "manager": "Old Mgr"}, response_type=None)
    assert created.status in (200, 201)
    shop_id = created.data["id"]

    # Actualizar si existe el método
    update_fn = getattr(shop_service, "update_shop", None)
    if update_fn is None:
        pytest.skip("ShopService no expone update_shop; se omite este caso en esta implementación.")

    payload = {"address": "New Addr", "manager": "New Mgr"}
    upd = update_fn(shop_id=shop_id, shop=payload, response_type=None)
    assert upd.status in (200, 204, 201)

    # Si devuelve cuerpo actualizado, lo validamos
    data = getattr(upd, "data", None)
    if isinstance(data, dict):
        assert data.get("id", shop_id) == shop_id
        if "address" in data:
            assert data["address"] == "New Addr"
        if "manager" in data:
            assert data["manager"] == "New Mgr"
