from .notes.notes import notes_routes

from flask import Flask


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    app.register_blueprint(notes_routes)

    return app