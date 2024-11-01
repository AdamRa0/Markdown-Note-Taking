from pathlib import Path

import markdown
from flask import Blueprint, request, json, jsonify, render_template
from spellchecker import SpellChecker


notes_routes = Blueprint("notes", __name__, url_prefix="/api/v1/notes")

NOTES_DIR = Path(f"{Path.cwd()}/uploaded_notes")
TEMPLATES_DIR = Path(f"{Path.cwd()}/app/templates")



@notes_routes.route("/")
def view_notes():
    files = [f.name for f in NOTES_DIR.iterdir() if f.is_file()]

    res = f"data: {files}"

    response = json.dumps(res)

    return jsonify(response), 200


@notes_routes.route("/create", methods=["POST"])
def create_note():
    data = json.loads(request.data.decode("UTF-8"))

    title = data.get("title")
    body = data.get("body")

    with open(f"{NOTES_DIR}/{title}.md", "w+") as writer:
        writer.write(body)

    with open(f"{TEMPLATES_DIR}/{title}.html", "w+") as writer:
        html = markdown.markdown(body)
        writer.write(html)

    return jsonify("Note created successfully"), 201


@notes_routes.route("/<note>")
def get_note(note: str):
    return render_template(f"{note}.html")


@notes_routes.route("/check-grammer/<note>")
def check_grammer_in_note(note: str):
    checker = SpellChecker()

    with open(f"{NOTES_DIR}/{note}.md", "r") as reader:
        content = reader.read()

    mispelled_words = checker.unknown(content)

    response = f"Misplaced Words coupled with suggestions: {[(word, checker.candidates(word)) for word in mispelled_words if word != ' ' and word != '\n']}"

    return jsonify(response), 200


@notes_routes.route("/upload", methods=["POST"])
def upload_note():
    pass


@notes_routes.route("/delete", methods=["DELETE"])
def delete_note():
    pass