import pytest

@pytest.mark.smoke
def test_create_movie_success(services, shop_id):
    movie_service = services["movie_service"]

    payload = {
        "name": "Inception",
        "director": "Christopher Nolan",
        "genres": ["Sci-Fi", "Thriller"],
        "shop": shop_id,
    }
    resp = movie_service.create_movie(movie=payload, response_type=None)
    assert resp.status in (200, 201)

    data = resp.data
    assert isinstance(data, dict)
    expected_keys = {"id", "name", "director", "shop"}
    assert expected_keys.issubset(data.keys())
    assert isinstance(data["id"], int)
    assert isinstance(data["name"], str)
    assert isinstance(data["director"], str)
    assert isinstance(data["shop"], int)
    assert data["name"] == "Inception"
    assert data["director"] == "Christopher Nolan"
    assert data["shop"] == shop_id


def test_create_movie_with_genres_with_invalid_type(services, shop_id):
    movie_service = services["movie_service"]

    invalid_payload = {
        "name": "Invalid Movie",
        "director": "Nobody",
        "genres": "Drama",
        "shop": shop_id,
    }
    resp = movie_service.create_movie(movie=invalid_payload, response_type=dict)
    assert resp.status == 422


def test_create_movie_invalid_body_format(services, shop_id):
    movie_service = services["movie_service"]

    invalid_payload = {
        "name": "Bad Movie",
        "director": "Nobody",
        "genres": "Drama",
        "shop": shop_id,
    }
    resp = movie_service.create_movie(movie=invalid_payload, response_type=dict)
    assert resp.status == 422, f"Esperaba 422 y recibí {resp.status}"
