import pytest
from src.models.services.movie_service import MovieService
from src.models.services.shop_service import ShopService

@pytest.fixture
def movie_service():
    return MovieService()

@pytest.fixture
def shop_service():
    return ShopService()

def _mk_shop(shop_service):
    r = shop_service.add_shop({"address": "Loc VAL", "manager": "Nora"}, response_type=None)
    assert r.status in (200, 201)
    return r.data["id"]

def _mk_movie(movie_service, shop_id):
    payload = {"name": "The Prestige", "director": "Christopher Nolan", "genres": ["Drama"], "shop": shop_id}
    r = movie_service.create_movie(payload, response_type=None)
    assert r.status in (200, 201)
    return r.data["id"]

def test_update_movie_validation_error(movie_service, shop_service):
    """
    TC-008: PUT /movies/{id} with invalid body should return 422
    """
    sid = _mk_shop(shop_service)
    mid = _mk_movie(movie_service, sid)


    invalid_body = {
        "name": "The Prestige (Broken)",
        "genres": "Drama", 
        "shop": sid
    }

    resp = movie_service.update_movie(mid, invalid_body, response_type=None)
    assert resp.status == 422
