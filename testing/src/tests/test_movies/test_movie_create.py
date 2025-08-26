import pytest
from src.models.services.movie_service import MovieService
from src.models.services.shop_service import ShopService

# ---------- Fixtures ----------
@pytest.fixture
def movie_service():
    return MovieService()

@pytest.fixture
def shop_service():
    return ShopService()

# ---------- Helpers ----------
def _mk_shop(shop_service: ShopService, address="Cine Center", manager="Eva") -> int:
    """Crea un shop válido y devuelve su id."""
    resp = shop_service.add_shop({"address": address, "manager": manager}, response_type=None)
    assert resp.status in (200, 201)
    return resp.data["id"]

# ---------- Tests de creación de movies ----------

@pytest.mark.smoke
def test_create_movie_success(movie_service: MovieService, shop_service: ShopService):
    """
    TC-006 — POST /movies success
    Crea una movie válida y valida el esquema básico de respuesta.
    """
    shop_id = _mk_shop(shop_service)

    payload = {
        "name": "Inception",
        "director": "Christopher Nolan",
        "genres": ["Sci-Fi", "Thriller"],
        "shop": shop_id,
    }
    resp = movie_service.create_movie(movie=payload, response_type=None)
    assert resp.status in (200, 201)

    data = resp.data
    assert isinstance(data, dict)

    # Claves mínimas esperadas
    expected_keys = {"id", "name", "director", "shop"}
    assert expected_keys.issubset(data.keys())

    # Tipos y valores
    assert isinstance(data["id"], int)
    assert isinstance(data["name"], str)
    assert isinstance(data["director"], str)
    assert isinstance(data["shop"], int)

    assert data["name"] == "Inception"
    assert data["director"] == "Christopher Nolan"
    assert data["shop"] == shop_id


def test_create_movie_validation_error(movie_service: MovieService, shop_service: ShopService):
    """
    TC-005 — POST /movies (validation error)
    Rechaza payload inválido (genres como string).
    """
    shop_id = _mk_shop(shop_service, address="Validation Shop", manager="Vera")

    invalid_payload = {
        "name": "Invalid Movie",
        "director": "Nobody",
        "genres": "Drama",        # ❌ debería ser list[str]
        "shop": shop_id,
    }
    resp = movie_service.create_movie(movie=invalid_payload, response_type=dict)
    assert resp.status in (400, 422)


def test_create_movie_invalid_body_format(movie_service: MovieService, shop_service: ShopService):
    """
    TC-020 — POST /movies (invalid body format)
    Mismo patrón de invalidez que TC-005 para cubrir contrato de formato.
    """
    shop_id = _mk_shop(shop_service, address="Shop T20", manager="Carla")

    invalid_payload = {
        "name": "Bad Movie",
        "director": "Nobody",
        "genres": "Drama",        # ❌ debería ser list[str]
        "shop": shop_id,
    }
    resp = movie_service.create_movie(movie=invalid_payload, response_type=dict)
    assert resp.status in (400, 422), f"Esperaba 400/422 y recibí {resp.status}"
