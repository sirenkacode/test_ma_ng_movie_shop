import pytest

@pytest.mark.smoke
def test_get_movie_by_id_success(services, shop_id):
    movie_service = services["movie_service"]

    create_payload = {
        "name": "Memento",
        "director": "Christopher Nolan",
        "genres": ["Thriller"],
        "shop": shop_id,
    }
    r = movie_service.create_movie(create_payload, response_type=None)
    assert r.status in (200, 201)
    movie_id = r.data["id"]

    resp = movie_service.get_movie(movie_id, response_type=dict)
    assert resp.status == 200

    data = resp.data
    assert isinstance(data, dict)
    for key in ("id", "name", "director", "genres", "shop"):
        assert key in data
    assert data["id"] == movie_id
    assert data["name"] == create_payload["name"]
    assert data["director"] == create_payload["director"]
    assert data["shop"] == shop_id
    assert isinstance(data["genres"], list) and len(data["genres"]) >= 1


def test_get_movie_by_id_nonexistent_returns_404(services):
    movie_service = services["movie_service"]
    resp = movie_service.get_movie(999_999_999, response_type=dict)
    assert resp.status == 404
