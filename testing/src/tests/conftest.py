# testing/src/tests/conftest.py
from dotenv import load_dotenv
import pytest
from src.models.services.shop_service import ShopService
from src.models.services.movie_service import MovieService

load_dotenv()

@pytest.fixture
def shop_service(services):
    return services["shop_service"]

@pytest.fixture
def movie_service(services):
    return services["movie_service"]

@pytest.fixture
def services():
    return {
        "shop_service": ShopService(),
        "movie_service": MovieService(),
    }

@pytest.fixture
def shop_id(services):
    shop_service = services["shop_service"]
    resp = shop_service.add_shop({"address": "Cine Center", "manager": "Eva"}, response_type=None)
    _id = resp.data["id"]
    yield _id
    # Cleanup best-effort
    try:
        shop_service.delete_shop(_id)
    except Exception:
        pass
