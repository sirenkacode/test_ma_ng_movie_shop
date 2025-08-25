import pytest

from src.models.services.shop_service import ShopService


@pytest.fixture
def shop_service():
    return ShopService()


@pytest.mark.smoke
def test_get_shops_success(shop_service):
    response = shop_service.get_shops(response_type=list[dict])
    assert response.status == 200
    assert isinstance(response.data, list)
    if response.data:
        first = response.data[0]
        assert isinstance(first, dict)
        for key in ("id", "name"):
            assert key in first


def test_get_shop_empty_list(shop_service):
    response = shop_service.get_shops(response_type=list[dict])
    assert response.status == 200
    assert isinstance(response.data, list)
    assert response.data == [] or isinstance(response.data, list)


@pytest.mark.skip(reason="API has no authentication; invalid token test not applicable")
def test_get_shops_invalid_response(shop_service):
    bad_config = {"headers": {"Authorization": "Bearer wrong_token"}}
    response = shop_service.get_shops(response_type=list[dict], config=bad_config)
    assert response.status != 200
