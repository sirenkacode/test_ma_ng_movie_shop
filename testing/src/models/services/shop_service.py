from typing import Type
from src.base.service_base import ServiceBase
from src.models.responses.base.response import T, Response


class ShopService(ServiceBase):
    def __init__(self):
        super().__init__("shops")

    def get_shops(
        self,
        response_type: Type[T],
        config: dict | None = None
    ) -> Response[T]:
        config = config or self.default_config
        return self.get(
            self.url,
            config=config,
            response_model=response_type,
        )

    def add_shop(
        self,
        shop: dict,
        response_type: Type[T],
        config: dict | None = None
    ) -> Response[T]:
        config = config or self.default_config
        return self.post(
            self.url,
            shop,
            config=config,
            response_model=response_type,
        )

    def get_shop_movies(
        self,
        shop_id: int | str,
        response_type: Type[T],
        params: dict | None = None,
        config: dict | None = None
    ) -> Response[T]:
        """
        GET /shops/{id}/movies
        Admite filtros vía params (ej. {"available": "true"}).
        """
        cfg = config or self.default_config
        if params:
            cfg = {**cfg, "params": params}
        return self.get(
            f"{self.url}/{shop_id}/movies",
            config=cfg,
            response_model=response_type,
        )
