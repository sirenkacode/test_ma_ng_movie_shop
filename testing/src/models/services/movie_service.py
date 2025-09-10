from typing import Type
from src.base.service_base import ServiceBase
from src.models.responses.base.response import T, Response


class MovieService(ServiceBase):
    def __init__(self):
        # Base path → /movies
        super().__init__("movies")

    def get_movies(
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

    def get_movie(
        self,
        movie_id: int | str,
        response_type: Type[T],
        config: dict | None = None
    ) -> Response[T]:
        config = config or self.default_config
        return self.get(
            f"{self.url}/{movie_id}",
            config=config,
            response_model=response_type,
        )

    def create_movie(
        self,
        movie: dict,
        response_type: Type[T],
        config: dict | None = None
    ) -> Response[T]:
        config = config or self.default_config
        return self.post(
            self.url,
            movie,
            config=config,
            response_model=response_type,
        )

    def update_movie(
        self,
        movie_id: int | str,
        movie: dict,
        response_type: Type[T],
        config: dict | None = None
    ) -> Response[T]:
        config = config or self.default_config
        return self.put(
            f"{self.url}/{movie_id}",
            movie,
            config=config,
            response_model=response_type,
        )

    def delete_movie(
        self,
        movie_id: int | str,
        response_type: Type[T],
        config: dict | None = None
    ) -> Response[T]:
        config = config or self.default_config
        return self.delete(
            f"{self.url}/{movie_id}",
            config=config,
            response_model=response_type,
        )

    def search(
        self, 
        name: str, 
        response_type=list[dict], 
        config: dict | None = None
    ):
        cfg = {"params": {"name": name}}
        if config:
            cfg.update(config)
        return self.get(
        f"{self.base_url}/search/movies",
        config=cfg,
        response_model=response_type,
    )

    def transfer(
        self,
        movie_id: int | str,
        body: dict,
        response_type: Type[T],
        config: dict | None = None
    ) -> Response[T]:
        config = config or self.default_config
        return self.post(
            f"{self.url}/{movie_id}/transfer",
            body,
            config=config,
            response_model=response_type,
        )
