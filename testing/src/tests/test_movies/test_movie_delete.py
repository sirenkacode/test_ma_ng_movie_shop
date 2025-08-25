import os
import pytest
from src.models.services.movie_service import MovieService


@pytest.fixture
def movie_service():
    return MovieService()

@pytest.mark.smoke
def test_delete_movie_success(client):
    shop = client.post("/shops", json={"address": "Blockbuster", "manager": "Hank"}).json()
    shop_id = shop["id"]

    movie = client.post("/movies", json={
        "name": "Titanic",
        "director": "James Cameron",
        "genres": ["Romance", "Drama"],
        "shop": shop_id
    }).json()
    movie_id = movie["id"]

    response = client.delete(f"/movies/{movie_id}")

    assert response.status_code == 204
    response_check = client.get(f"/movies/{movie_id}")
    assert response_check.status_code == 404
