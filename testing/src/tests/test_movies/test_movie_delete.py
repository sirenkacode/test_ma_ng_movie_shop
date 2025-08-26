import pytest
from src.models.services.movie_service import MovieService
from src.models.services.shop_service import ShopService

@pytest.fixture
def movie_service():
    return MovieService()

@pytest.fixture
def shop_service():
    return ShopService()

def _mk_shop(shop_service: ShopService) -> int:
    r = shop_service.add_shop({"address": "Loc DEL", "manager": "Leo"}, response_type=None)
    assert r.status in (200, 201)
    return r.data["id"]

def _mk_movie(movie_service: MovieService, shop_id: int) -> int:
    payload = {"name": "Dunkirk", "director": "Christopher Nolan", "genres": ["War"], "shop": shop_id}
    r = movie_service.create_movie(payload, response_type=None)
    assert r.status in (200, 201)
    return r.data["id"]

@pytest.mark.smoke
def test_delete_movie_success(movie_service: MovieService, shop_service: ShopService):
    """
    Happy path: DELETE /movies/{id} borra una movie existente.
    """
    # Precondiciones
    sid = _mk_shop(shop_service)
    mid = _mk_movie(movie_service, sid)

    # Acción
    deleted = movie_service.delete_movie(movie_id=mid, response_type=None)
    assert deleted.status in (200, 204)

    # Verificación: el id ya no debe aparecer en la lista
    listing = movie_service.get_movies(response_type=list[dict])
    assert listing.status == 200
    assert isinstance(listing.data, list)
    assert all(m.get("id") != mid for m in listing.data)

def test_delete_movie_non_existing_id(movie_service: MovieService):
    """
    TC-018 — DELETE /movies/{id} (non-existing id)
    Debe devolver error adecuado para un id inexistente.
    """
    resp = movie_service.delete_movie(movie_id=999_999_999, response_type=dict)
    # Aceptamos los códigos de error comunes según backend (404/422/400).
    assert resp.status in (404, 422, 400)
