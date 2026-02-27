import os
from urllib.parse import quote_plus

from flask import Flask
from flask_cors import CORS

from .errors import register_error_handlers
from .extensions import db
from .routes import api


def _build_database_uri() -> str:
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    username = quote_plus(os.getenv("DB_USERNAME", ""))
    password = quote_plus(os.getenv("DB_PASSWORD", ""))
    database = os.getenv("DB_DATABASE", "jira_development")
    connect_timeout = os.getenv("DB_CONNECT_TIMEOUT_MS", "5000")

    timeout_seconds = max(1, int(connect_timeout) // 1000)

    if password:
        auth = f"{username}:{password}"
    else:
        auth = username

    return (
        f"postgresql+psycopg2://{auth}@{host}:{port}/{database}"
        f"?connect_timeout={timeout_seconds}"
    )


def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = _build_database_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False

    CORS(app)

    db.init_app(app)
    register_error_handlers(app)

    app.register_blueprint(api)

    with app.app_context():
        db.create_all()

    return app
