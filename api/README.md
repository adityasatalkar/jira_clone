# Flask API structure

The backend has been migrated to Python/Flask.

## Runtime

- Entry point: `run.py`
- App package: `flask_app/`
- Start command: `python3 run.py`
- Test command: `NODE_ENV=test DB_DATABASE=jira_test python3 run.py`

## Files

| File or folder | Description |
| --- | --- |
| `run.py` | Loads env vars and starts the Flask app on `PORT` (default `3000`). |
| `requirements.txt` | Python dependencies for backend runtime. |
| `flask_app/__init__.py` | App factory, DB URI setup, CORS, error handlers, blueprint registration. |
| `flask_app/extensions.py` | Shared Flask extensions (`SQLAlchemy`). |
| `flask_app/models.py` | SQLAlchemy models (`Project`, `User`, `Issue`, `Comment`) and relationships. |
| `flask_app/routes.py` | API routes matching existing client contract (`/authentication/guest`, `/project`, `/issues`, `/comments`, `/currentUser`). |
| `flask_app/auth.py` | JWT signing/verification and auth decorator for private routes. |
| `flask_app/serializers.py` | Response serialization with camelCase fields expected by the React client. |
| `flask_app/validators.py` | Input validation helpers used by route handlers. |
| `flask_app/seeds.py` | Guest/test account seed flows and test DB reset helper. |
| `flask_app/errors.py` | API error types and consistent error response shape. |

## Notes

- Tables are auto-created at startup (`db.create_all()`), consistent with previous non-migration setup.
