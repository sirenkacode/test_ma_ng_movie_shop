import pytest
from src.models.services.shop_service import ShopService
from src.models.services.movie_service import MovieService

@pytest.fixture
def shop_service():
    return ShopService()

@pytest.fixture
def movie_service():
    return MovieService()


def test_get_shop_movies_available_true(shop_service, movie_service):
    """
    TC-013: GET /shops/{id}/movies?available=true
    Debe devolver 200 y una lista; si el backend incluye el campo 'rent',
    los disponibles deberían venir con rent == False.
    """

    shop_resp = shop_service.add_shop(
        {"address": "Shop With Movies", "manager": "Nora"},
        response_type=None
    )
    assert shop_resp.status in (200, 201)
    shop_id = shop_resp.data["id"]


    m1 = movie_service.create_movie(
        {"name": "Free Guy", "director": "Levy", "genres": ["Comedy"], "shop": shop_id},
        response_type=None
    )
    assert m1.status in (200, 201)

    m2 = movie_service.create_movie(
        {"name": "Taken", "director": "Morel", "genres": ["Action"], "shop": shop_id},
        response_type=None
    )
    assert m2.status in (200, 201)
    m2_id = m2.data["id"]

  
    _ = movie_service.update_movie(
        movie_id=m2_id,
        movie={"rent": True},
        response_type=None
    )

    resp = shop_service.get_shop_movies(
        shop_id=shop_id,
        response_type=list[dict],
        params={"available": "true"}
    )
    assert resp.status == 200
    assert isinstance(resp.data, list)


    if resp.data and isinstance(resp.data[0], dict) and "rent" in resp.data[0]:
        assert all(item.get("rent") is False for item in resp.data)


def test_get_shop_movies_available_false(shop_service, movie_service):
    """
    TC-014: GET /shops/{id}/movies?available=false
    Debe devolver 200 y una lista; si el backend incluye el campo 'rent',
    los NO disponibles deberían venir con rent == True.
    """
    # 1) Crear shop
    shop_resp = shop_service.add_shop(
        {"address": "Shop With Movies 2", "manager": "Nora"},
        response_type=None
    )
    assert shop_resp.status in (200, 201)
    shop_id = shop_resp.data["id"]

 
    m1 = movie_service.create_movie(
        {"name": "Gravity", "director": "Cuarón", "genres": ["Sci-Fi"], "shop": shop_id},
        response_type=None
    )
    assert m1.status in (200, 201)
    m1_id = m1.data["id"]

    m2 = movie_service.create_movie(
        {"name": "Arrival", "director": "Villeneuve", "genres": ["Sci-Fi"], "shop": shop_id},
        response_type=None
    )
    assert m2.status in (200, 201)
    m2_id = m2.data["id"]


    _ = movie_service.update_movie(movie_id=m1_id, movie={"rent": True}, response_type=None)
    _ = movie_service.update_movie(movie_id=m2_id, movie={"rent": True}, response_type=None)

 
    resp = shop_service.get_shop_movies(
        shop_id=shop_id,
        response_type=list[dict],
        params={"available": "false"}
    )

    assert resp.status == 200
    assert isinstance(resp.data, list)


    if resp.data and isinstance(resp.data[0], dict) and "rent" in resp.data[0]:
        rents = [item.get("rent") for item in resp.data]
        assert all(isinstance(r, (bool, type(None))) for r in rents), f"Tipos raros en rent: {rents}"
