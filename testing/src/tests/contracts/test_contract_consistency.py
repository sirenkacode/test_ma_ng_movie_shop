import pytest
from src.models.services.movie_service import MovieService

@pytest.fixture
def movie_service():
    return MovieService()


def _is_json_content_type(headers: dict) -> bool:
    ct = headers.get("content-type") or headers.get("Content-Type") or ""
    return "application/json" in ct.lower()


def _assert_error_shape(body: dict):
    """
    Acepta esquemas de error comunes:
    - {"detail": "..."} (FastAPI)
    - {"message": "..."} / {"error": "..."}
    - {"errors": [...]}  (lista con strings o dicts)
    """
    assert isinstance(body, dict), "El cuerpo de error debe ser JSON objeto"

    keys = set(body.keys())
    expected_any = {"detail", "message", "error", "errors"}
    assert keys & expected_any, f"Estructura de error inesperada: keys={keys}"

    if "errors" in body:
        errs = body["errors"]
        assert isinstance(errs, (list, dict)), "errors debe ser lista o dict"
        # si es lista, aceptamos strings o dicts con 'msg'/'loc' típicos de pydantic
        if isinstance(errs, list):
            for item in errs:
                assert isinstance(item, (str, dict)), f"Elemento de 'errors' inesperado: {item!r}"


# TC-016 — Contract & consistency (headers / error shape)
def test_contract_consistency_headers_and_error_shape(movie_service):
    """
    TC-016: Validar headers JSON y forma de error (422/400) ante body inválido.
    """
    # Forzamos 422/400: 'genres' como string en lugar de lista
    invalid_payload = {
        "name": "Invalid Payload",
        "director": "Nobody",
        "genres": "Drama",  # <- debería ser lista
        "shop": -1,         # <- fuerza validación también
    }
    resp = movie_service.create_movie(movie=invalid_payload, response_type=dict)

    # 1) Status de error aceptable
    assert resp.status in (400, 422), f"Esperaba 400/422 y recibí {resp.status}"

    # 2) Headers deben ser JSON
    assert hasattr(resp, "headers") and isinstance(resp.headers, dict), "No hay headers en la respuesta"
    assert _is_json_content_type(resp.headers), f"Content-Type no es JSON: {resp.headers}"

    # 3) Forma del error (flexible a tu backend)
    body = getattr(resp, "data", None)
    assert body is not None, "La respuesta de error no tiene cuerpo"
    _assert_error_shape(body)


# TC-017 — Response contract consistency (headers & error body)
def test_response_contract_consistency_headers_and_error_body(movie_service):
    """
    TC-017: Validar consistencia de headers y cuerpo de error en distintos escenarios.
    Escenarios:
      A) DELETE con id inexistente -> 404/422/400
      B) UPDATE con payload inválido -> 422/400
    """
    # A) DELETE inexistente
    del_resp = movie_service.delete_movie(movie_id=999999999, response_type=dict)
    assert del_resp.status in (400, 404, 422)
    assert hasattr(del_resp, "headers") and isinstance(del_resp.headers, dict)
    assert _is_json_content_type(del_resp.headers)
    del_body = getattr(del_resp, "data", None)
    assert del_body is not None
    _assert_error_shape(del_body)

    # B) UPDATE inválido (faltan campos obligatorios / tipos incorrectos)
    upd_resp = movie_service.update_movie(
        movie_id=999999999,
        movie={"shop": "not-an-int"},   # tipo incorrecto + id inexistente
        response_type=dict
    )
    assert upd_resp.status in (400, 404, 422)
    assert hasattr(upd_resp, "headers") and isinstance(upd_resp.headers, dict)
    assert _is_json_content_type(upd_resp.headers)
    upd_body = getattr(upd_resp, "data", None)
    assert upd_body is not None
    _assert_error_shape(upd_body)
