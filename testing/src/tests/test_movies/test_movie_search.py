import pytest

@pytest.mark.smoke
def test_search_movies_finds_created_movie(services, shop_id):
    movie_service = services["movie_service"]
    payload = {"name": "The Matrix", "director": "The Wachowskis", "genres": ["Sci-Fi"], "shop": shop_id}
    r = movie_service.create_movie(payload, response_type=None)
    assert r.status in (200, 201)
    mid = r.data["id"]

    resp = movie_service.search(name="Matrix", response_type=list[dict])
    assert resp.status == 200
    data = resp.data
    assert isinstance(data, list)
    assert any(
        isinstance(m, dict)
        and m.get("id") == mid
        and m.get("name") == payload["name"]
        and m.get("director") == payload["director"]
        and isinstance(m.get("genres"), list)
        and m.get("shop") == shop_id
        for m in data
    )

def test_search_movies_no_matches_returns_empty_list(services):
    movie_service = services["movie_service"]
    resp = movie_service.search(name="__no_match_token__", response_type=list[dict])
    assert resp.status == 200
    assert isinstance(resp.data, list) and len(resp.data) == 0

@pytest.mark.parametrize("query", ["matrix", "MATRIX", "MaTrIx"])
def test_search_movies_is_case_insensitive(services, shop_id, query):
    movie_service = services["movie_service"]
    r = movie_service.create_movie(
        {"name": "The Matrix", "director": "The Wachowskis", "genres": ["Sci-Fi"], "shop": shop_id},
        response_type=None,
    )
    assert r.status in (200, 201)
    mid = r.data["id"]

    resp = movie_service.search(name=query, response_type=list[dict])
    assert resp.status == 200
    assert any(isinstance(m, dict) and m.get("id") == mid for m in resp.data)
