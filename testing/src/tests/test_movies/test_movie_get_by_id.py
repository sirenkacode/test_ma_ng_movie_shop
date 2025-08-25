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
    resp = shop_service.add_shop({"address": "Loc GET", "manager": "Sara"}, response_type=None)
    assert resp.status in (200, 201)
    return resp.data["id"]

def _mk_movie(movie_service, shop_id: int):
    payload = {"name": "Memento", "director": "Christopher Nolan", "genres": ["Thriller"], "shop": shop_id}
    resp = movie_service.create_movie(payload, response_type=None)
    assert resp.status in (200, 201)
    return resp.data["id"], payload

@pytest.mark.smoke
def test_get_movie_by_id_success(movie_service, shop_service):
    # precondiciones: 
    shop_id = _mk_shop(shop_service)
    movie_id, created_payload = _mk_movie(movie_service, shop_id)

    # acción: 
    resp = movie_service.get_movie(movie_id, response_type=dict)
    assert resp.status == 200
    assert isinstance(resp.data, dict)

    # verificaciones:
    for key in ("id", "name", "director", "genres", "shop"):
        assert key in resp.data
    assert resp.data["id"] == movie_id
    assert resp.data["name"] == created_payload["name"]
    assert resp.data["director"] == created_payload["director"]
    assert resp.data["shop"] == shop_id
    assert isinstance(resp.data["genres"], list) and len(resp.data["genres"]) >= 1
