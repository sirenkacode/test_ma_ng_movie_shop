import pytest
from src.models.services.movie_service import MovieService

@pytest.fixture
def movie_service():
    return MovieService()

@pytest.mark.smoke
def test_get_movies_success(movie_service):
    response = movie_service.get_movies(response_type=list[dict])
    assert response.status == 200
    assert isinstance(response.data, list)

    if response.data:
        first = response.data[0]
        assert isinstance(first, dict)
    
        for key in ("id", "name", "director", "genres", "shop"):
            assert key in first

def test_get_movies_empty_list(movie_service):
    response = movie_service.get_movies(response_type=list[dict])
    assert response.status == 200
    assert isinstance(response.data, list)

def test_get_movies_ignores_auth_header(movie_service):
 
    bad_config = {"headers": {"Authorization": "Bearer wrong_token"}}
    response = movie_service.get_movies(response_type=list[dict], config=bad_config)
    assert response.status == 200
    assert isinstance(response.data, list)
