import logging
from dataclasses import dataclass, field
from typing import Any, Dict

from flask import jsonify, request


@dataclass
class ApiError(Exception):
    message: str
    code: str = "INTERNAL_ERROR"
    status: int = 500
    data: Dict[str, Any] = field(default_factory=dict)


class RouteNotFoundError(ApiError):
    def __init__(self, original_url: str):
        super().__init__(
            message=f"Route '{original_url}' does not exist.",
            code="ROUTE_NOT_FOUND",
            status=404,
        )


class EntityNotFoundError(ApiError):
    def __init__(self, entity_name: str):
        super().__init__(message=f"{entity_name} not found.", code="ENTITY_NOT_FOUND", status=404)


class BadUserInputError(ApiError):
    def __init__(self, data: Dict[str, Any]):
        super().__init__(
            message="There were validation errors.",
            code="BAD_USER_INPUT",
            status=400,
            data=data,
        )


class InvalidTokenError(ApiError):
    def __init__(self, message: str = "Authentication token is invalid."):
        super().__init__(message=message, code="INVALID_TOKEN", status=401)


def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def handle_api_error(error: ApiError):
        return (
            jsonify(
                {
                    "error": {
                        "message": error.message,
                        "code": error.code,
                        "status": error.status,
                        "data": error.data,
                    }
                }
            ),
            error.status,
        )

    @app.errorhandler(404)
    def handle_404(_error):
        not_found_error = RouteNotFoundError(request.path)
        return (
            jsonify(
                {
                    "error": {
                        "message": not_found_error.message,
                        "code": not_found_error.code,
                        "status": not_found_error.status,
                        "data": {},
                    }
                }
            ),
            404,
        )

    @app.errorhandler(Exception)
    def handle_unknown_error(error: Exception):
        logging.exception("Unhandled API error", exc_info=error)
        return (
            jsonify(
                {
                    "error": {
                        "message": "Something went wrong, please contact our support.",
                        "code": "INTERNAL_ERROR",
                        "status": 500,
                        "data": {},
                    }
                }
            ),
            500,
        )
