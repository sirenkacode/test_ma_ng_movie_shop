import pytest
from src.models.services.shop_service import ShopService

@pytest.fixture
def shop_service():
    return ShopService()

def test_delete_shop_success(shop_service):
    """
    DELETE /shops/{id} success (solo si tu SDK expone delete_shop).
    Si no existe delete_shop en ShopService, se marca skipped.
    """
    # Crear
    created = shop_service.add_shop({"address": "Shop To Delete", "manager": "Dana"}, response_type=None)
    assert created.status in (200, 201)
    shop_id = created.data["id"]

    # Borrar si existe el método
    delete_fn = getattr(shop_service, "delete_shop", None)
    if delete_fn is None:
        pytest.skip("ShopService no expone delete_shop; se omite este caso en esta implementación.")

    deleted = delete_fn(shop_id=shop_id, response_type=None)
    assert deleted.status in (200, 204)

    # Verificar que no esté en la lista (si tu SDK tiene get_shops)
    if hasattr(shop_service, "get_shops"):
        listing = shop_service.get_shops(response_type=list[dict])
        assert listing.status == 200
        assert all(s.get("id") != shop_id for s in listing.data or [])
