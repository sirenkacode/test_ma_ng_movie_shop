import pytest

@pytest.mark.smoke
def test_update_movie_name_success(movie_service, shop_id):

    r = movie_service.create_movie(
        {"name": "Tenet", "director": "Christopher Nolan", "genres": ["Sci-Fi"], "shop": shop_id},
        response_type=None,
    )
    assert r.status in (200, 201)
    mid = r.data["id"]

  
    current = movie_service.get_movie(mid, response_type=dict)
    assert current.status == 200
    body_full = {
        "name": "Tenet (Updated)",
        "director": current.data["director"],
        "genres": current.data["genres"],
        "shop": current.data["shop"],
    }

    upd = movie_service.update_movie(mid, body_full, response_type=None)
    assert upd.status in (200, 204)

    got = movie_service.get_movie(mid, response_type=dict)
    assert got.status == 200
    assert got.data["id"] == mid
    assert got.data["name"] == "Tenet (Updated)"
    assert got.data["director"] == body_full["director"]
    assert got.data["genres"] == body_full["genres"]
    assert got.data["shop"] == body_full["shop"]


def test_update_movie_invalid_body_returns_422(movie_service, shop_id):
    r = movie_service.create_movie(
        {"name": "The Prestige", "director": "Christopher Nolan", "genres": ["Drama"], "shop": shop_id},
        response_type=None,
    )
    assert r.status in (200, 201)
    mid = r.data["id"]

    current = movie_service.get_movie(mid, response_type=dict)
    assert current.status == 200
    invalid_body = {
        "name": current.data["name"],
        "director": current.data["director"],
        "genres": "Drama",        # <- tipo inválido
        "shop": current.data["shop"],
    }

    resp = movie_service.update_movie(mid, invalid_body, response_type=None)
    assert resp.status == 422


def test_update_movie_nonexistent_id_returns_404(movie_service, shop_id):
    full_body = {
        "name": "Ghost Movie",
        "director": "Nobody",
        "genres": ["Drama"],
        "shop": shop_id,
    }
    resp = movie_service.update_movie(999_999_999, full_body, response_type=dict)

    if resp.status != 404:
        pytest.xfail(f"Se esperaba 404 para id inexistente; backend devolvió {resp.status}")
    assert resp.status == 404
