from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from .models import Comment, Issue, Project, User


def _serialize_datetime(value: Optional[datetime]) -> Optional[str]:
    if value is None:
        return None
    return value.isoformat()


def serialize_user(user: User) -> Dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "avatarUrl": user.avatarUrl,
        "createdAt": _serialize_datetime(user.createdAt),
        "updatedAt": _serialize_datetime(user.updatedAt),
        "projectId": user.projectId,
    }


def serialize_comment(comment: Comment, include_user: bool = False) -> Dict:
    data = {
        "id": comment.id,
        "body": comment.body,
        "createdAt": _serialize_datetime(comment.createdAt),
        "updatedAt": _serialize_datetime(comment.updatedAt),
        "userId": comment.userId,
        "issueId": comment.issueId,
    }
    if include_user:
        data["user"] = serialize_user(comment.user)
    return data


def serialize_issue_partial(issue: Issue) -> Dict:
    return {
        "id": issue.id,
        "title": issue.title,
        "type": issue.type,
        "status": issue.status,
        "priority": issue.priority,
        "listPosition": issue.listPosition,
        "createdAt": _serialize_datetime(issue.createdAt),
        "updatedAt": _serialize_datetime(issue.updatedAt),
        "userIds": sorted([user.id for user in issue.users]),
    }


def serialize_issue(issue: Issue, include_users: bool = False, include_comments: bool = False) -> Dict:
    user_ids = sorted([user.id for user in issue.users])

    data = {
        "id": issue.id,
        "title": issue.title,
        "type": issue.type,
        "status": issue.status,
        "priority": issue.priority,
        "listPosition": issue.listPosition,
        "description": issue.description,
        "descriptionText": issue.descriptionText,
        "estimate": issue.estimate,
        "timeSpent": issue.timeSpent,
        "timeRemaining": issue.timeRemaining,
        "createdAt": _serialize_datetime(issue.createdAt),
        "updatedAt": _serialize_datetime(issue.updatedAt),
        "reporterId": issue.reporterId,
        "projectId": issue.projectId,
        "userIds": user_ids,
    }

    if include_users:
        data["users"] = [serialize_user(user) for user in issue.users]

    if include_comments:
        data["comments"] = [
            serialize_comment(comment, include_user=True)
            for comment in sorted(issue.comments, key=lambda c: c.createdAt or datetime.min)
        ]

    return data


def serialize_project(project: Project, partial_issues: bool = True) -> Dict:
    issues: List[Dict]
    if partial_issues:
        issues = [serialize_issue_partial(issue) for issue in project.issues]
    else:
        issues = [serialize_issue(issue) for issue in project.issues]

    return {
        "id": project.id,
        "name": project.name,
        "url": project.url,
        "description": project.description,
        "category": project.category,
        "createdAt": _serialize_datetime(project.createdAt),
        "updatedAt": _serialize_datetime(project.updatedAt),
        "users": [serialize_user(user) for user in project.users],
        "issues": issues,
    }


def serialize_project_basic(project: Project) -> Dict:
    return {
        "id": project.id,
        "name": project.name,
        "url": project.url,
        "description": project.description,
        "category": project.category,
        "createdAt": _serialize_datetime(project.createdAt),
        "updatedAt": _serialize_datetime(project.updatedAt),
    }
