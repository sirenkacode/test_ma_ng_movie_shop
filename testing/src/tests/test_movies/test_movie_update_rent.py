import os
import pytest
from src.models.services.movie_service import MovieService


@pytest.fixture
def movie_service():
    return MovieService()

@pytest.mark.smoke
def test_update_rent_movie_success(client):
    shop = client.post("/shops", json={"address": "Cinema Plaza", "manager": "Grace"}).json()
    shop_id = shop["id"]

    movie = client.post("/movies", json={
        "name": "Gladiator",
        "director": "Ridley Scott",
        "genres": ["Drama"],
        "shop": shop_id
    }).json()
    movie_id = movie["id"]
    response = client.patch(f"/movies/{movie_id}/rent", json={"rent": True})
    assert response.status_code == 200
    data = response.json()
    assert data["rent"] is True
