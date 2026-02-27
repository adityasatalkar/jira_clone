import os

from dotenv import load_dotenv

from flask_app import create_app


load_dotenv()
app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "3000"))
    debug = os.getenv("NODE_ENV", "development") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug)
