import pytest

@pytest.mark.smoke
def test_get_movies_success(services):
    movie_service = services["movie_service"]
    response = movie_service.get_movies(response_type=list[dict])
    assert response.status == 200
    assert isinstance(response.data, list)
    if response.data:
        first = response.data[0]
        assert isinstance(first, dict)
        for key in ("id", "name", "director", "genres", "shop"):
            assert key in first

def test_get_movies_returns_list_type(services):
    movie_service = services["movie_service"]
    response = movie_service.get_movies(response_type=list[dict])
    assert response.status == 200
    assert isinstance(response.data, list)
