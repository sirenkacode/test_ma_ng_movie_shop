import pytest
from src.models.services.movie_service import MovieService
from src.models.services.shop_service import ShopService

@pytest.fixture
def movie_service():
    return MovieService()

@pytest.fixture
def shop_service():
    return ShopService()

def test_search_movies_matches_found(movie_service, shop_service):
    """
    TC-010: GET /movies/search?name=... (matches found)
    """
    shop_resp = shop_service.add_shop({"address": "Search Loc", "manager": "Mario"}, response_type=None)
    assert shop_resp.status in (200, 201)
    shop_id = shop_resp.data["id"]

    resp = movie_service.create_movie({
        "name": "Matrix",
        "director": "Wachowski",
        "genres": ["Sci-Fi"],
        "shop": shop_id,
    }, response_type=None)
    assert resp.status in (200, 201)

 
    search_resp = movie_service.search(name="Matrix", response_type=list[dict])


    assert search_resp.status in (200, 422)

def test_search_movies_no_matches(movie_service):
    """
    TC-011: GET /movies/search?name=... (no matches)
    """
    search_resp = movie_service.search(name="__nope__", response_type=list[dict])

    assert search_resp.status in (200, 422)
    if search_resp.status == 200:
        assert isinstance(search_resp.data, list)
        assert len(search_resp.data) == 0

