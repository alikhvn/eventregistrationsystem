"""Minimal Flask web app for the Event Registration System."""

from flask import Flask, render_template, request

from db import get_events, init_db, register_participant

app = Flask(__name__)
init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    is_error = False

    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        event_id = request.form.get("event_id", type=int)
        success, message = register_participant(event_id, name, email)
        is_error = not success

    return render_template(
        "index.html",
        events=get_events(),
        message=message,
        is_error=is_error,
    )


if __name__ == "__main__":
    app.run(debug=True)
