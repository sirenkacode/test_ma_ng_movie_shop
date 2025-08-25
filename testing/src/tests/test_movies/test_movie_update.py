import os
import pytest
from src.models.services.movie_service import MovieService


@pytest.fixture
def movie_service():
    return MovieService()

@pytest.mark.smoke
def test_update_movie_success(client):
    shop = client.post("/shops", json={"address": "Film St", "manager": "Frank"}).json()
    shop_id = shop["id"]

    movie = client.post("/movies", json={
        "name": "Matrix",
        "director": "Wachowski",
        "genres": ["Sci-Fi"],
        "shop": shop_id
    }).json()
    movie_id = movie["id"]

    update_payload = {
        "name": "Matrix Reloaded",
        "director": "Wachowski Sisters",
        "genres": ["Sci-Fi", "Action"]
    }
    response = client.put(f"/movies/{movie_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Matrix Reloaded"
    assert "Action" in data["genres"]
