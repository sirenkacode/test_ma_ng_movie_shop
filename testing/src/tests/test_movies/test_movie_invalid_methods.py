import pytest
from src.models.services.movie_service import MovieService

@pytest.fixture
def movie_service():
    return MovieService()


def test_movies_endpoint_unsupported_method(movie_service):
    """
    TC-021 — Unsupported method on /movies
    Intenta invocar /movies con un método no soportado (PATCH).
    Esperado: 405 Method Not Allowed (acepta 400/404 como variantes).
    Si el SDK no expone un cliente HTTP crudo, se salta el caso sin romper el orden.
    """
    # Intentar descubrir un cliente HTTP crudo que tenga .patch(...)
    client = None
    for attr in ("client", "_client", "session", "_session", "http", "_http"):
        c = getattr(movie_service, attr, None)
        if c is not None and hasattr(c, "patch"):
            client = c
            break

    if client is None:
        pytest.skip("MovieService no expone un cliente HTTP para probar métodos arbitrarios en /movies")

    resp = client.patch("/movies", json={})
    assert resp.status_code in (405, 400, 404), f"Status inesperado: {resp.status_code}"
