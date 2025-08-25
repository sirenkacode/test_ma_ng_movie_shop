import os
from http import HTTPMethod
from time import time
from typing import Any, Dict, Optional, Type, TypeVar, List, get_args
import requests
from dotenv import load_dotenv
from pydantic import BaseModel
from requests import Session

from src.models.responses.base.response import Response

T = TypeVar("T")


def _issubclass_safe(obj: Any, cls: type) -> bool:
    """issubclass sin romperse si obj no es un tipo."""
    try:
        return isinstance(obj, type) and issubclass(obj, cls)
    except Exception:
        return False


class ServiceBase(Session):
    """
    Base class for API services.
    Should be inherited by specific service implementations.

    Example:
        class UserService(ServiceBase):
            def __init__(self):
                super().__init__("users")
    """

    def __init__(self, path: str = "", base_url: str = "") -> None:
        super().__init__()
        load_dotenv(override=True)

        self.store = Session()  
        self.base_url = base_url or os.getenv("BASE_URL")
        if not self.base_url:
            raise ValueError("A valid base_url must be provided.")

     
        self.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )
        self.url = f"{self.base_url}/{path.strip('/')}"

        self.default_config: Dict[str, Any] = {}
      
        self.headers.update(self.headers)
        self.cookies.update(self.cookies)

  
    def get(self, url: str, response_model: Type[T] = None, **kwargs: Any) -> Response[T]:
        return self._request(HTTPMethod.GET, url, response_model=response_model, **kwargs)

    def post(
        self,
        url: str,
        data: Optional[Any] = None,
        response_model: Type[T] = None,
        **kwargs: Any,
    ) -> Response[T]:
        return self._request(HTTPMethod.POST, url, data, response_model=response_model, **kwargs)

    def put(
        self,
        url: str,
        data: Optional[Any] = None,
        response_model: Type[T] = None,
        **kwargs: Any,
    ) -> Response[T]:
        return self._request(HTTPMethod.PUT, url, data, response_model=response_model, **kwargs)

    def patch(
        self,
        url: str,
        data: Optional[Any] = None,
        response_model: Type[T] = None,
        **kwargs: Any,
    ) -> Response[T]:
        return self._request(HTTPMethod.PATCH, url, data, response_model=response_model, **kwargs)

    def delete(self, url: str, response_model: Type[T] = None, **kwargs: Any) -> Response[T]:
        return self._request(HTTPMethod.DELETE, url, response_model=response_model, **kwargs)

    def options(self, url: str, response_model: Type[T] = None, **kwargs: Any) -> Response[T]:
        return self._request(HTTPMethod.OPTIONS, url, response_model=response_model, **kwargs)

    def head(self, url: str, response_model: Type[T] = None, **kwargs: Any) -> Response[T]:
        return self._request(HTTPMethod.HEAD, url, response_model=response_model, **kwargs)

    def trace(self, url: str, response_model: Type[T] = None, **kwargs: Any) -> Response[T]:
        return self._request(HTTPMethod.TRACE, url, response_model=response_model, **kwargs)

    def connect(self, url: str, response_model: Type[T] = None, **kwargs: Any) -> Response[T]:
        return self._request(HTTPMethod.CONNECT, url, response_model=response_model, **kwargs)

 
    def _request(
        self,
        method: str | HTTPMethod,
        url: str,
        data: Optional[Any] = None,
        config: Optional[Dict[str, Any]] = None,
        response_model: Type[T] = None,
        **kwargs: Any,
    ) -> Response[T]:
        config = config or self.default_config
        start_time = int(time() * 1000)

       
        has_model_dump = data is not None and hasattr(data, "model_dump")
        json_payload = data.model_dump(exclude_none=True) if has_model_dump else data

      
        meth_name = method.name.lower() if isinstance(method, HTTPMethod) else str(method).lower()
        response = getattr(super(), meth_name)(url, json=json_payload, **config, **kwargs)
        end_time = int(time() * 1000)

      
        try:
            raw_data = response.json()
        except ValueError:
            raw_data = None 

       
        if response_model in (None, dict, list):
          
            parsed_data = raw_data

        elif isinstance(raw_data, list):
           
            args = get_args(response_model) 
            if args and _issubclass_safe(args[0], BaseModel):
                model = args[0]
                parsed_data = [model.model_validate(item) for item in raw_data]
            else:
               
                parsed_data = raw_data

        else:
           
            if _issubclass_safe(response_model, BaseModel):
                parsed_data = response_model.model_validate(raw_data)
            else:
               
                parsed_data = raw_data

        return Response(
            status=response.status_code,
            headers=response.headers,
            data=parsed_data,
            response_time=end_time - start_time,
        )
