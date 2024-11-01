from .notes.notes import notes_routes

from flask import Flask
from pathlib import Path


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.config["SAVED_NOTES"] = "uploaded_notes"

    notes_dir = Path(f"{Path.cwd()}/{app.config["SAVED_NOTES"]}")

    notes_dir.mkdir(exist_ok=True)

    app.register_blueprint(notes_routes)

    return app