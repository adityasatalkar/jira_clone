from .extensions import db
from .models import Comment, Issue, Project, User


def reset_database():
    db.drop_all()
    db.create_all()


def _create_users(project: Project, users):
    persisted_users = []
    for user in users:
        persisted = User(
            name=user["name"],
            email=user["email"],
            avatarUrl=user["avatarUrl"],
            project=project,
        )
        db.session.add(persisted)
        persisted_users.append(persisted)
    db.session.flush()
    return persisted_users


def create_guest_account() -> User:
    project = Project(
        name="singularity 1.0",
        url="https://www.atlassian.com/software/jira",
        description=(
            "Plan, track, and manage your agile and software development projects in Jira. "
            "Customize your workflow, collaborate, and release great software."
        ),
        category="software",
    )
    db.session.add(project)
    db.session.flush()

    users = _create_users(
        project,
        [
            {
                "email": "rick@jira.guest",
                "name": "Pickle Rick",
                "avatarUrl": "https://i.ibb.co/7JM1P2r/picke-rick.jpg",
            },
            {
                "email": "yoda@jira.guest",
                "name": "Baby Yoda",
                "avatarUrl": "https://i.ibb.co/6n0hLML/baby-yoda.jpg",
            },
            {
                "email": "gaben@jira.guest",
                "name": "Lord Gaben",
                "avatarUrl": "https://i.ibb.co/6RJ5hq6/gaben.jpg",
            },
        ],
    )

    issues_input = [
        {
            "title": "This is an issue of type: Task.",
            "type": "task",
            "status": "backlog",
            "priority": "4",
            "listPosition": 1,
            "description": "<p>Issue description for task.</p>",
            "estimate": 8,
            "timeSpent": 4,
            "timeRemaining": 4,
            "reporterId": users[1].id,
            "users": [users[0]],
        },
        {
            "title": "Click on an issue to see what's behind it.",
            "type": "task",
            "status": "backlog",
            "priority": "2",
            "listPosition": 2,
            "description": "<p>Open issue details modal for full context.</p>",
            "estimate": 5,
            "timeSpent": 2,
            "timeRemaining": 3,
            "reporterId": users[2].id,
            "users": [users[0]],
        },
        {
            "title": "Try dragging issues to different columns.",
            "type": "story",
            "status": "selected",
            "priority": "3",
            "listPosition": 1,
            "description": "<p>Move me across columns to update status.</p>",
            "estimate": 15,
            "timeSpent": 7,
            "timeRemaining": 8,
            "reporterId": users[1].id,
            "users": [users[1]],
        },
        {
            "title": "Each issue can have multiple assignees.",
            "type": "story",
            "status": "selected",
            "priority": "5",
            "listPosition": 2,
            "description": "<p>Assign both Pickle Rick and Lord Gaben.</p>",
            "estimate": 10,
            "timeSpent": 5,
            "timeRemaining": 5,
            "reporterId": users[0].id,
            "users": [users[0], users[2]],
        },
        {
            "title": "Track spent and remaining time.",
            "type": "task",
            "status": "inprogress",
            "priority": "1",
            "listPosition": 1,
            "description": "<p>Time tracking is available in issue details.</p>",
            "estimate": 12,
            "timeSpent": 11,
            "timeRemaining": 1,
            "reporterId": users[0].id,
            "users": [users[2]],
        },
        {
            "title": "Try leaving a comment on this issue.",
            "type": "task",
            "status": "done",
            "priority": "3",
            "listPosition": 1,
            "description": "<p>Comments help teams collaborate asynchronously.</p>",
            "estimate": 6,
            "timeSpent": 6,
            "timeRemaining": 0,
            "reporterId": users[2].id,
            "users": [users[1]],
        },
    ]

    issues = []
    for issue_data in issues_input:
        issue = Issue(
            title=issue_data["title"],
            type=issue_data["type"],
            status=issue_data["status"],
            priority=issue_data["priority"],
            listPosition=issue_data["listPosition"],
            description=issue_data["description"],
            estimate=issue_data["estimate"],
            timeSpent=issue_data["timeSpent"],
            timeRemaining=issue_data["timeRemaining"],
            reporterId=issue_data["reporterId"],
            project=project,
        )
        issue.users = issue_data["users"]
        db.session.add(issue)
        issues.append(issue)

    db.session.flush()

    comments = [
        {
            "body": "An old silent pond...\nA frog jumps into the pond,\nsplash! Silence again.",
            "issue": issues[0],
            "user": users[2],
        },
        {
            "body": "Autumn moonlight-\na worm digs silently\ninto the chestnut.",
            "issue": issues[1],
            "user": users[2],
        },
        {
            "body": "In the twilight rain\nthese brilliant-hued hibiscus -\nA lovely sunset.",
            "issue": issues[2],
            "user": users[1],
        },
    ]

    for comment_data in comments:
        db.session.add(
            Comment(
                body=comment_data["body"],
                issue=comment_data["issue"],
                user=comment_data["user"],
            )
        )

    db.session.commit()
    return users[2]


def create_test_account() -> User:
    project = Project(
        name="Project name",
        url="https://www.testurl.com",
        description="Project description",
        category="software",
    )
    db.session.add(project)
    db.session.flush()

    users = _create_users(
        project,
        [
            {
                "email": "gaben@jira.test",
                "name": "Gaben",
                "avatarUrl": "https://i.ibb.co/6RJ5hq6/gaben.jpg",
            },
            {
                "email": "yoda@jira.test",
                "name": "Yoda",
                "avatarUrl": "https://i.ibb.co/6n0hLML/baby-yoda.jpg",
            },
        ],
    )

    issue = Issue(
        title="Issue title 1",
        type="task",
        status="backlog",
        priority="1",
        listPosition=1,
        reporterId=users[0].id,
        project=project,
    )
    issue.users = [users[0]]
    db.session.add(issue)
    db.session.flush()

    db.session.add(
        Comment(
            body="Comment body",
            issue=issue,
            user=users[0],
        )
    )

    db.session.commit()
    return users[0]
