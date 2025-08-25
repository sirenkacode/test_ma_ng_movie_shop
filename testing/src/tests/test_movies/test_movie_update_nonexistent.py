import pytest
from src.models.services.movie_service import MovieService

@pytest.fixture
def movie_service():
    return MovieService()

def test_update_movie_nonexistent_id_returns_404_or_422(movie_service):
    nonexistent_id = 999999


    body_full = {
        "name": "Ghost Movie",
        "director": "Nobody",
        "genres": ["Drama"],
        "shop": 1  
    }

    resp = movie_service.update_movie(nonexistent_id, body_full, response_type=None)

    
    assert resp.status in (404, 422)
