from ast import literal_eval

from flask import Blueprint, request, json, jsonify


notes_routes = Blueprint("notes", __name__, url_prefix="/api/v1/notes")


@notes_routes.route("/")
def view_notes():
    return "View all notes route", 200


@notes_routes.route("/create", methods=["POST"])
def create_note():
    data = json.loads(request.data.decode("UTF-8"))

    title = data.get("title")
    body = data.get("body")

    with open(f"{title}.md", "w+") as writer:
        writer.write(body)

    return jsonify("Note created successfully"), 201


@notes_routes.route("/<note>")
def get_note(note: str):
    return "Get note route", 200


@notes_routes.route("/check-grammer/<note>")
def check_grammer_in_note(note: str):
    return "Chcek grammer note route", 200


@notes_routes.route("/upload", methods=["POST"])
def upload_note():
    pass


@notes_routes.route("/delete", methods=["DELETE"])
def delete_note():
    pass