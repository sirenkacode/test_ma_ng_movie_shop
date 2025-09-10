import pytest

@pytest.mark.smoke
def test_delete_movie_success(services, shop_id):
    movie_service = services["movie_service"]

    payload = {
        "name": "Dunkirk",
        "director": "Christopher Nolan",
        "genres": ["War"],
        "shop": shop_id,
    }
    r = movie_service.create_movie(payload, response_type=None)
    assert r.status in (200, 201)
    mid = r.data["id"]

    deleted = movie_service.delete_movie(movie_id=mid, response_type=None)
    assert deleted.status == 204

    listing = movie_service.get_movies(response_type=list[dict])
    assert listing.status == 200
    assert isinstance(listing.data, list)
    assert all(m.get("id") != mid for m in listing.data)

def test_delete_movie_non_existing_id(services):
    movie_service = services["movie_service"]
    resp = movie_service.delete_movie(movie_id=999_999_999, response_type=dict)
    assert resp.status == 404
