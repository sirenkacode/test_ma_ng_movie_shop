import os
import pytest
from src.models.services.movie_service import MovieService


@pytest.fixture
def movie_service():
    return MovieService()

@pytest.mark.smoke
def test_create_movie_success(client):
    shop_payload = {"address": "Cine Center", "manager": "Eva"}
    shop = client.post("/shops", json=shop_payload).json()
    shop_id = shop["id"]

    movie_payload = {
        "name": "Inception",
        "director": "Christopher Nolan",
        "genres": ["Sci-Fi", "Thriller"],
        "shop": shop_id
    }

    response = client.post("/movies", json=movie_payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Inception"
    assert data["director"] == "Christopher Nolan"
    assert "id" in data
    assert data["shop"] == shop_id
