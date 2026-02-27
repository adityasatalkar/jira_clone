from __future__ import annotations

import os
from typing import Any, Dict, List

from flask import Blueprint, g, jsonify, request
from sqlalchemy import func, or_
from sqlalchemy.orm import joinedload

from .auth import require_auth, sign_token
from .errors import BadUserInputError, EntityNotFoundError, RouteNotFoundError
from .extensions import db
from .models import Comment, Issue, Project, User
from .seeds import create_guest_account, create_test_account, reset_database
from .serializers import (
    serialize_comment,
    serialize_issue,
    serialize_project,
    serialize_project_basic,
    serialize_user,
)
from .validators import (
    validate_comment_payload,
    validate_issue_payload,
    validate_project_payload,
)


api = Blueprint("api", __name__)


@api.route("/authentication/guest", methods=["POST"])
def authentication_guest():
    user = create_guest_account()
    return jsonify({"authToken": sign_token({"sub": user.id})})


@api.route("/currentUser", methods=["GET"])
@require_auth
def current_user():
    return jsonify({"currentUser": serialize_user(g.current_user)})


@api.route("/project", methods=["GET"])
@require_auth
def get_project():
    project = (
        Project.query.options(
            joinedload(Project.users),
            joinedload(Project.issues).joinedload(Issue.users),
        )
        .filter(Project.id == g.current_user.projectId)
        .first()
    )

    if not project:
        raise EntityNotFoundError("Project")

    return jsonify({"project": serialize_project(project, partial_issues=True)})


@api.route("/project", methods=["PUT"])
@require_auth
def update_project():
    payload = request.get_json(silent=True) or {}
    errors = validate_project_payload(payload)
    if errors:
        raise BadUserInputError({"fields": errors})

    project = Project.query.filter(Project.id == g.current_user.projectId).first()
    if not project:
        raise EntityNotFoundError("Project")

    project.name = payload.get("name")
    project.url = payload.get("url")
    project.description = payload.get("description")
    project.category = payload.get("category")

    db.session.commit()
    return jsonify({"project": serialize_project_basic(project)})


@api.route("/issues", methods=["GET"])
@require_auth
def get_issues():
    search_term = (request.args.get("searchTerm") or "").strip()

    query = Issue.query.options(joinedload(Issue.users)).filter(
        Issue.projectId == g.current_user.projectId
    )

    if search_term:
        search_pattern = f"%{search_term}%"
        query = query.filter(
            or_(Issue.title.ilike(search_pattern), Issue.descriptionText.ilike(search_pattern))
        )

    issues = query.all()
    return jsonify({"issues": [serialize_issue(issue) for issue in issues]})


@api.route("/issues/<int:issue_id>", methods=["GET"])
@require_auth
def get_issue(issue_id: int):
    issue = (
        Issue.query.options(
            joinedload(Issue.users),
            joinedload(Issue.comments).joinedload(Comment.user),
        )
        .filter(Issue.id == issue_id)
        .first()
    )

    if not issue:
        raise EntityNotFoundError("Issue")

    return jsonify({"issue": serialize_issue(issue, include_users=True, include_comments=True)})


@api.route("/issues", methods=["POST"])
@require_auth
def create_issue():
    payload = request.get_json(silent=True) or {}
    errors = validate_issue_payload(payload, partial=False)
    if errors:
        raise BadUserInputError({"fields": errors})

    project_id = int(payload["projectId"])
    status = payload["status"]

    min_list_position = (
        db.session.query(func.min(Issue.listPosition))
        .filter(Issue.projectId == project_id, Issue.status == status)
        .scalar()
    )

    list_position = (min_list_position - 1) if min_list_position is not None else 1

    issue = Issue(
        title=payload.get("title"),
        type=payload.get("type"),
        status=status,
        priority=payload.get("priority"),
        listPosition=float(list_position),
        description=payload.get("description"),
        estimate=payload.get("estimate"),
        timeSpent=payload.get("timeSpent"),
        timeRemaining=payload.get("timeRemaining"),
        reporterId=int(payload.get("reporterId")),
        projectId=project_id,
    )

    issue.users = _resolve_users(payload)

    db.session.add(issue)
    db.session.commit()

    issue = Issue.query.options(joinedload(Issue.users)).filter(Issue.id == issue.id).first()
    return jsonify({"issue": serialize_issue(issue, include_users=True)})


@api.route("/issues/<int:issue_id>", methods=["PUT"])
@require_auth
def update_issue(issue_id: int):
    issue = Issue.query.options(joinedload(Issue.users)).filter(Issue.id == issue_id).first()
    if not issue:
        raise EntityNotFoundError("Issue")

    payload = request.get_json(silent=True) or {}
    errors = validate_issue_payload(payload, partial=True)
    if errors:
        raise BadUserInputError({"fields": errors})

    if "title" in payload:
        issue.title = payload.get("title")
    if "type" in payload:
        issue.type = payload.get("type")
    if "status" in payload:
        issue.status = payload.get("status")
    if "priority" in payload:
        issue.priority = payload.get("priority")
    if "listPosition" in payload:
        issue.listPosition = float(payload.get("listPosition"))
    if "description" in payload:
        issue.description = payload.get("description")
    if "estimate" in payload:
        issue.estimate = payload.get("estimate")
    if "timeSpent" in payload:
        issue.timeSpent = payload.get("timeSpent")
    if "timeRemaining" in payload:
        issue.timeRemaining = payload.get("timeRemaining")
    if "reporterId" in payload:
        issue.reporterId = int(payload.get("reporterId"))
    if "projectId" in payload and payload.get("projectId") is not None:
        issue.projectId = int(payload.get("projectId"))

    if "userIds" in payload or "users" in payload:
        issue.users = _resolve_users(payload)

    db.session.commit()

    issue = Issue.query.options(joinedload(Issue.users)).filter(Issue.id == issue.id).first()
    return jsonify({"issue": serialize_issue(issue, include_users=True)})


@api.route("/issues/<int:issue_id>", methods=["DELETE"])
@require_auth
def delete_issue(issue_id: int):
    issue = Issue.query.options(joinedload(Issue.users)).filter(Issue.id == issue_id).first()
    if not issue:
        raise EntityNotFoundError("Issue")

    issue_data = serialize_issue(issue, include_users=True)
    db.session.delete(issue)
    db.session.commit()

    return jsonify({"issue": issue_data})


@api.route("/comments", methods=["POST"])
@require_auth
def create_comment():
    payload = request.get_json(silent=True) or {}
    errors = validate_comment_payload(payload, partial=False)

    if payload.get("issueId") is None:
        errors["issueId"] = "This field is required"
    if payload.get("userId") is None:
        errors["userId"] = "This field is required"

    if errors:
        raise BadUserInputError({"fields": errors})

    comment = Comment(
        body=payload.get("body"),
        issueId=int(payload.get("issueId")),
        userId=int(payload.get("userId")),
    )
    db.session.add(comment)
    db.session.commit()

    return jsonify({"comment": serialize_comment(comment)})


@api.route("/comments/<int:comment_id>", methods=["PUT"])
@require_auth
def update_comment(comment_id: int):
    comment = Comment.query.filter(Comment.id == comment_id).first()
    if not comment:
        raise EntityNotFoundError("Comment")

    payload = request.get_json(silent=True) or {}
    errors = validate_comment_payload(payload, partial=False)

    if errors:
        raise BadUserInputError({"fields": errors})

    comment.body = payload.get("body")
    db.session.commit()

    return jsonify({"comment": serialize_comment(comment)})


@api.route("/comments/<int:comment_id>", methods=["DELETE"])
@require_auth
def delete_comment(comment_id: int):
    comment = Comment.query.filter(Comment.id == comment_id).first()
    if not comment:
        raise EntityNotFoundError("Comment")

    comment_data = serialize_comment(comment)
    db.session.delete(comment)
    db.session.commit()

    return jsonify({"comment": comment_data})


@api.route("/test/reset-database", methods=["DELETE"])
def test_reset_database():
    _assert_test_mode()
    reset_database()
    return jsonify(True)


@api.route("/test/create-account", methods=["POST"])
def test_create_account():
    _assert_test_mode()
    user = create_test_account()
    return jsonify({"authToken": sign_token({"sub": user.id})})



def _assert_test_mode():
    if os.getenv("NODE_ENV") != "test":
        raise RouteNotFoundError(request.path)


def _resolve_users(payload: Dict[str, Any]) -> List[User]:
    user_ids = _extract_user_ids(payload)
    if not user_ids:
        return []

    users = User.query.filter(User.id.in_(user_ids)).all()

    users_by_id = {user.id: user for user in users}
    return [users_by_id[user_id] for user_id in user_ids if user_id in users_by_id]



def _extract_user_ids(payload: Dict[str, Any]) -> List[int]:
    user_ids_payload: Any = None

    if isinstance(payload.get("userIds"), list):
        user_ids_payload = payload.get("userIds")
    elif isinstance(payload.get("users"), list):
        user_ids_payload = [user.get("id") for user in payload.get("users") if isinstance(user, dict)]

    if not isinstance(user_ids_payload, list):
        return []

    normalized: List[int] = []
    seen = set()
    for user_id in user_ids_payload:
        try:
            parsed = int(user_id)
        except (TypeError, ValueError):
            continue

        if parsed in seen:
            continue

        seen.add(parsed)
        normalized.append(parsed)

    return normalized
