import pytest
from src.models.services.movie_service import MovieService
from src.models.services.shop_service import ShopService

@pytest.fixture
def movie_service():
    return MovieService()

@pytest.fixture
def shop_service():
    return ShopService()

@pytest.mark.smoke
def test_create_movie_success(movie_service, shop_service):

    shop_payload = {"address": "Cine Center", "manager": "Eva"}
    shop_resp = shop_service.add_shop(shop=shop_payload, response_type=None)
    assert shop_resp.status in (200, 201)
    shop_id = shop_resp.data.get("id")
    assert shop_id is not None

    movie_payload = {
        "name": "Inception",
        "director": "Christopher Nolan",
        "genres": ["Sci-Fi", "Thriller"],
        "shop": shop_id,
    }
    resp = movie_service.create_movie(movie=movie_payload, response_type=None)
    assert resp.status in (200, 201)

    data = resp.data
    assert isinstance(data, dict)
    for key in ("id", "name", "director", "shop"):
        assert key in data
    assert data["name"] == "Inception"
    assert data["director"] == "Christopher Nolan"
    assert data["shop"] == shop_id

def test_create_movie_validation_error(movie_service, shop_service):
    """
    TC-005: POST /movies (validation error)
    """

    shop_payload = {"address": "Validation Shop", "manager": "Vera"}
    shop_resp = shop_service.add_shop(shop=shop_payload, response_type=None)
    assert shop_resp.status in (200, 201)
    shop_id = shop_resp.data.get("id")
    assert shop_id is not None

  
    invalid_payload = {
        "name": "Invalid Movie",
        "director": "Nobody",
        "genres": "Drama",
        "shop": shop_id,
    }

    resp = movie_service.create_movie(movie=invalid_payload, response_type=None)

    assert resp.status in (400, 422)

def test_create_movie_invalid_body_format(movie_service, shop_service):
    """
    TC-020 — POST /movies (invalid body format)
    Intenta crear una movie con body inválido:
    - 'genres' enviado como string en lugar de lista.
    Esperado: 422/400 y que no se cree la película.
    """
    # Precondición: crear un shop válido
    shop_resp = shop_service.add_shop({"address": "Shop T20", "manager": "Carla"}, response_type=None)
    assert shop_resp.status in (200, 201)
    shop_id = shop_resp.data["id"]

    # Payload inválido
    invalid_payload = {
        "name": "Bad Movie",
        "director": "Nobody",
        "genres": "Drama",   # ❌ debería ser lista de strings
        "shop": shop_id,
    }

    resp = movie_service.create_movie(movie=invalid_payload, response_type=dict)

    # Validar respuesta de error
    assert resp.status in (400, 422), f"Esperaba 400/422 y recibí {resp.status}"
