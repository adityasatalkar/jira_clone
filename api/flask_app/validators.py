import re
from typing import Any, Dict, Iterable, Optional

from .constants import ISSUE_PRIORITIES, ISSUE_STATUSES, ISSUE_TYPES, PROJECT_CATEGORIES


EMAIL_REGEX = re.compile(r".+@.+\..+")
URL_REGEX = re.compile(
    r"^(?:http(s)?://)?[\w.-]+(?:\.[\w.-]+)+[\w\-._~:/?#[\]@!$&'()*+,;=.]+$"
)


def _is_nil_or_empty(value: Any) -> bool:
    return value is None or value == ""


def _add_error(errors: Dict[str, str], field: str, message: str):
    if field not in errors:
        errors[field] = message


def _to_int(value: Any) -> Optional[int]:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _to_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def validate_comment_payload(payload: Dict[str, Any], partial: bool = False) -> Dict[str, str]:
    errors: Dict[str, str] = {}

    if not partial or "body" in payload:
        body = payload.get("body")
        if _is_nil_or_empty(body):
            _add_error(errors, "body", "This field is required")
        elif len(str(body)) > 50000:
            _add_error(errors, "body", "Must be at most 50000 characters")

    return errors


def validate_project_payload(payload: Dict[str, Any]) -> Dict[str, str]:
    errors: Dict[str, str] = {}

    name = payload.get("name")
    category = payload.get("category")
    url = payload.get("url")

    if _is_nil_or_empty(name):
        _add_error(errors, "name", "This field is required")
    elif len(str(name)) > 100:
        _add_error(errors, "name", "Must be at most 100 characters")

    if _is_nil_or_empty(category):
        _add_error(errors, "category", "This field is required")
    elif str(category) not in PROJECT_CATEGORIES:
        _add_error(
            errors,
            "category",
            f"Must be one of: {', '.join(sorted(PROJECT_CATEGORIES))}",
        )

    if not _is_nil_or_empty(url) and not URL_REGEX.match(str(url)):
        _add_error(errors, "url", "Must be a valid URL")

    return errors


def _validate_choice(
    errors: Dict[str, str],
    payload: Dict[str, Any],
    field: str,
    options: Iterable[str],
    partial: bool,
):
    if not partial or field in payload:
        value = payload.get(field)
        if _is_nil_or_empty(value):
            _add_error(errors, field, "This field is required")
        elif str(value) not in options:
            _add_error(errors, field, f"Must be one of: {', '.join(sorted(options))}")


def validate_issue_payload(payload: Dict[str, Any], partial: bool = False) -> Dict[str, str]:
    errors: Dict[str, str] = {}

    if not partial or "title" in payload:
        title = payload.get("title")
        if _is_nil_or_empty(title):
            _add_error(errors, "title", "This field is required")
        elif len(str(title)) > 200:
            _add_error(errors, "title", "Must be at most 200 characters")

    _validate_choice(errors, payload, "type", ISSUE_TYPES, partial)
    _validate_choice(errors, payload, "status", ISSUE_STATUSES, partial)
    _validate_choice(errors, payload, "priority", ISSUE_PRIORITIES, partial)

    required_int_fields = ["reporterId"]
    if not partial:
        required_int_fields.append("projectId")

    for field in required_int_fields:
        if not partial or field in payload:
            if _to_int(payload.get(field)) is None:
                _add_error(errors, field, "This field is required")

    if "listPosition" in payload and _to_float(payload.get("listPosition")) is None:
        _add_error(errors, "listPosition", "This field is required")

    for optional_int in ["estimate", "timeSpent", "timeRemaining"]:
        if optional_int in payload and payload.get(optional_int) is not None:
            if _to_int(payload.get(optional_int)) is None:
                _add_error(errors, optional_int, "Must be a number")

    if "userIds" in payload and not isinstance(payload.get("userIds"), list):
        _add_error(errors, "userIds", "Must be an array")

    return errors


def validate_user_payload(name: Any, email: Any) -> Dict[str, str]:
    errors: Dict[str, str] = {}

    if _is_nil_or_empty(name):
        _add_error(errors, "name", "This field is required")
    elif len(str(name)) > 100:
        _add_error(errors, "name", "Must be at most 100 characters")

    if _is_nil_or_empty(email):
        _add_error(errors, "email", "This field is required")
    elif len(str(email)) > 200:
        _add_error(errors, "email", "Must be at most 200 characters")
    elif not EMAIL_REGEX.match(str(email)):
        _add_error(errors, "email", "Must be a valid email")

    return errors
