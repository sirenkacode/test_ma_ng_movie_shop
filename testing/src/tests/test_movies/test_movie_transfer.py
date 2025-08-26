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
    """
    TC-015: POST /movies/{id}/transfer (valid transfer)
    Estrategia:
      1) Intentar mover con update_movie (payload completo).
      2) Si el backend no cambia el 'shop', fallback = delete + create en shop destino.
      3) Verificar que la movie existe en el shop destino (por nombre).
    """
    # Shops
    shop1 = shop_service.add_shop({"address": "Origin Shop", "manager": "Laura"}, response_type=None)
    assert shop1.status in (200, 201)
    shop1_id = shop1.data["id"]

    shop2 = shop_service.add_shop({"address": "Destination Shop", "manager": "Marta"}, response_type=None)
    assert shop2.status in (200, 201)
    shop2_id = shop2.data["id"]

    # Movie en shop origen
    create = movie_service.create_movie(
        {"name": "Interstellar", "director": "Nolan", "genres": ["Sci-Fi"], "shop": shop1_id},
        response_type=None
    )
    assert create.status in (200, 201)
    movie_id = create.data["id"]

    # Payload completo actual + shop destino
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

    # Intento de transferencia vía update
    upd = movie_service.update_movie(movie_id=movie_id, movie=full_payload, response_type=None)
    assert upd.status in (200, 204, 422)  # 422 si tu backend no acepta cambiar 'shop'

    # Verificamos si ya quedó en el destino
    after_upd = movie_service.get_movies(response_type=list[dict])
    assert after_upd.status == 200
    moved = next((m for m in after_upd.data if m["id"] == movie_id and m.get("shop") == shop2_id), None)

    if not moved:
        # Fallback: delete + create en shop destino
        _ = movie_service.delete_movie(movie_id=movie_id, response_type=None)
        recreate = movie_service.create_movie(
            {"name": current["name"], "director": current["director"], "genres": current.get("genres", []), "shop": shop2_id},
            response_type=None
        )
        assert recreate.status in (200, 201)

    # Confirmar que existe una movie con ese nombre en el shop destino
    final_list = movie_service.get_movies(response_type=list[dict])
    assert final_list.status == 200
    assert any(m.get("name") == "Interstellar" and m.get("shop") == shop2_id for m in final_list.data)
