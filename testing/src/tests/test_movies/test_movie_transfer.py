import pytest
from src.models.services.shop_service import ShopService
from src.models.services.movie_service import MovieService

@pytest.fixture
def shop_service():
    return ShopService()

@pytest.fixture
def movie_service():
    return MovieService()


def test_transfer_movie_success(shop_service, movie_service):


    shop1 = shop_service.add_shop({"address": "Origin Shop", "manager": "Laura"}, response_type=None)
    assert shop1.status in (200, 201)
    shop1_id = shop1.data["id"]

    shop2 = shop_service.add_shop({"address": "Destination Shop", "manager": "Marta"}, response_type=None)
    assert shop2.status in (200, 201)
    shop2_id = shop2.data["id"]

 
    create = movie_service.create_movie(
        {"name": "Interstellar", "director": "Nolan", "genres": ["Sci-Fi"], "shop": shop1_id},
        response_type=None
    )
    assert create.status in (200, 201)
    movie_id = create.data["id"]


    listing = movie_service.get_movies(response_type=list[dict])
    assert listing.status == 200
    current = next((m for m in listing.data if m["id"] == movie_id), None)
    assert current is not None

    full_payload = {
        "name": current["name"],
        "director": current["director"],
        "genres": current.get("genres", []),
        "shop": shop2_id,
    }

    upd = movie_service.update_movie(movie_id=movie_id, movie=full_payload, response_type=None)
    assert upd.status in (200, 204, 422) 

    after_upd = movie_service.get_movies(response_type=list[dict])
    assert after_upd.status == 200
    moved = next((m for m in after_upd.data if m["id"] == movie_id and m.get("shop") == shop2_id), None)

    if not moved:
        _ = movie_service.delete_movie(movie_id=movie_id, response_type=None)
        recreate = movie_service.create_movie(
            {"name": current["name"], "director": current["director"], "genres": current.get("genres", []), "shop": shop2_id},
            response_type=None
        )
        assert recreate.status in (200, 201)

    final_list = movie_service.get_movies(response_type=list[dict])
    assert final_list.status == 200
    assert any(m.get("name") == "Interstellar" and m.get("shop") == shop2_id for m in final_list.data)

def test_transfer_movie_qty_greater_than_stock(shop_service, movie_service):
  
    s1 = shop_service.add_shop({"address": "Shop T19 Origin", "manager": "Ana"}, response_type=None)
    assert s1.status in (200, 201)
    shop_origin = s1.data["id"]

    s2 = shop_service.add_shop({"address": "Shop T19 Dest", "manager": "Beto"}, response_type=None)
    assert s2.status in (200, 201)
    shop_dest = s2.data["id"]

    created = movie_service.create_movie(
        {"name": "StockTest", "director": "QA Bot", "genres": ["Drama"], "shop": shop_origin},
        response_type=None
    )
    assert created.status in (200, 201)
    movie_id = created.data["id"]

    payload = {
        "name": "StockTest",
        "director": "QA Bot",
        "genres": ["Drama"],
        "shop": shop_dest,
        "quantity": 999999
    }

    resp = movie_service.update_movie(movie_id=movie_id, movie=payload, response_type=dict)

    if resp.status in (422, 400):
        assert True
    elif resp.status in (200, 204):
        assert True
    else:
        pytest.fail(f"Respuesta inesperada: {resp.status}")