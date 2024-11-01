from flask import Blueprint


notes_routes = Blueprint("notes", __name__, url_prefix="/api/v1/notes")


@notes_routes.route("/")
def view_notes():
    return "View all notes route", 200


@notes_routes.route("/create")
def create_note():
    return "Create note route", 200


@notes_routes.route("/<note>")
def get_note(note: str):
    return "Get note route", 200


@notes_routes.route("/check-grammer/<note>")
def check_grammer_in_note(note: str):
    return "Chcek grammer note route", 200