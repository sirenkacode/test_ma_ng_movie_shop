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
    r = shop_service.add_shop({"address": "Loc UPD", "manager": "Mia"}, response_type=None)
    assert r.status in (200, 201)
    return r.data["id"]

def _mk_movie(movie_service, shop_id):
    payload = {"name": "Tenet", "director": "Christopher Nolan", "genres": ["Sci-Fi"], "shop": shop_id}
    r = movie_service.create_movie(payload, response_type=None)
    assert r.status in (200, 201)
    return r.data["id"]

@pytest.mark.smoke
def test_update_movie_name_success(movie_service, shop_service):
    # Precondiciones
    sid = _mk_shop(shop_service)
    mid = _mk_movie(movie_service, sid)

    current = movie_service.get_movie(mid, response_type=dict)
    assert current.status == 200
    body_full = {
        "name": "Tenet (Updated)",
        "director": current.data["director"],
        "genres": current.data["genres"],
        "shop": current.data["shop"],
    }

    # Acción
    upd = movie_service.update_movie(mid, body_full, response_type=None)
    assert upd.status in (200, 204)

    # Verificación
    got = movie_service.get_movie(mid, response_type=dict)
    assert got.status == 200
    assert got.data["id"] == mid
    assert got.data["name"] == "Tenet (Updated)"
    assert got.data["director"] == body_full["director"]
    assert got.data["genres"] == body_full["genres"]
    assert got.data["shop"] == body_full["shop"]
