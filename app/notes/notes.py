import os
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
    if 'file' not in request.files:
        return jsonify("File not uploaded"), 400

    file = request.files['file']

    if file.filename == "":
        return jsonify("No selected file"), 400

    filename = file.filename

    filename_without_extension = os.path.splitext(filename)[0]

    file_content = file.read().decode("utf-8")

    file.save(f"{NOTES_DIR}/{filename}")

    with open(f"{TEMPLATES_DIR}/{filename_without_extension}.html", "w+") as writer:
        html = markdown.markdown(file_content)
        writer.write(html)

    return jsonify("Note uploaded"), 200


@notes_routes.route("/delete/<note>", methods=["DELETE"])
def delete_note(note: str):
    try:
        os.remove(f"{NOTES_DIR}/{note}.md")
        os.remove(f"{TEMPLATES_DIR}/{note}.html")
        return jsonify("Note deleted"), 204
    except FileNotFoundError:
        return jsonify("Note not found"), 404