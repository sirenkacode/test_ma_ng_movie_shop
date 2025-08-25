import pytest
from src.models.services.movie_service import MovieService

@pytest.fixture
def movie_service():
    return MovieService()

def test_get_movie_by_id_nonexistent_returns_404(movie_service):
    """
    TC-003: GET /movies/{id} non-existent
    """
    nonexistent_id = 999999

    resp = movie_service.get_movie(nonexistent_id, response_type=dict)

    assert resp.status in (404, 422)
