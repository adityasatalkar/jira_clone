import re
from datetime import datetime, timezone

from sqlalchemy import event

from .extensions import db


HTML_TAG_REGEX = re.compile(r"<[^>]+>")


def utcnow():
    return datetime.now(timezone.utc)


issue_users_user = db.Table(
    "issue_users_user",
    db.Column("issueId", db.Integer, db.ForeignKey("issue.id"), primary_key=True),
    db.Column("userId", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)


class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String, nullable=True)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String, nullable=False)

    createdAt = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    updatedAt = db.Column(
        db.DateTime(timezone=True),
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )

    issues = db.relationship("Issue", back_populates="project", cascade="all, delete-orphan")
    users = db.relationship("User", back_populates="project", cascade="all, delete-orphan")


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    avatarUrl = db.Column(db.String(2000), nullable=False)

    createdAt = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    updatedAt = db.Column(
        db.DateTime(timezone=True),
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )

    projectId = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=True)
    project = db.relationship("Project", back_populates="users")

    comments = db.relationship("Comment", back_populates="user")
    issues = db.relationship("Issue", secondary=issue_users_user, back_populates="users")


class Issue(db.Model):
    __tablename__ = "issue"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    priority = db.Column(db.String, nullable=False)
    listPosition = db.Column(db.Float, nullable=False)

    description = db.Column(db.Text, nullable=True)
    descriptionText = db.Column(db.Text, nullable=True)

    estimate = db.Column(db.Integer, nullable=True)
    timeSpent = db.Column(db.Integer, nullable=True)
    timeRemaining = db.Column(db.Integer, nullable=True)

    createdAt = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    updatedAt = db.Column(
        db.DateTime(timezone=True),
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )

    reporterId = db.Column(db.Integer, nullable=False)
    projectId = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)

    project = db.relationship("Project", back_populates="issues")
    comments = db.relationship("Comment", back_populates="issue", cascade="all, delete-orphan")
    users = db.relationship("User", secondary=issue_users_user, back_populates="issues")


class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)

    createdAt = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    updatedAt = db.Column(
        db.DateTime(timezone=True),
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )

    userId = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    issueId = db.Column(db.Integer, db.ForeignKey("issue.id", ondelete="CASCADE"), nullable=False)

    user = db.relationship("User", back_populates="comments")
    issue = db.relationship("Issue", back_populates="comments")


@event.listens_for(Issue, "before_insert")
@event.listens_for(Issue, "before_update")
def set_issue_description_text(_mapper, _connection, target: Issue):
    if target.description is None:
        target.descriptionText = None
        return
    target.descriptionText = HTML_TAG_REGEX.sub("", target.description)
