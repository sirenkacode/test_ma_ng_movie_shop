import pytest
from src.models.services.movie_service import MovieService

@pytest.fixture
def movie_service():
    return MovieService()


def test_contract_consistency_headers(movie_service):
    """
    TC-017: Contract headers
    Valida que las respuestas incluyan encabezados básicos de contrato.
    Ejemplo: Content-Type = application/json
    """
    resp = movie_service.get_movies(response_type=list[dict])
    assert resp.status == 200

    headers = getattr(resp, "headers", None)
    assert headers is not None, "No se encontraron headers en la respuesta"

    # Validar que el Content-Type sea application/json
    content_type = headers.get("content-type") or headers.get("Content-Type")
    assert content_type is not None
    assert "application/json" in content_type.lower()
