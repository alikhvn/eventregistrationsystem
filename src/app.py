"""Minimal Flask web app for the Event Registration System."""

from flask import Flask, render_template, request

from models import register_participant, seed_events

app = Flask(__name__)

# In-memory storage is enough for this lab; data resets on restart.
events = seed_events()


@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    is_error = False

    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        event_id = request.form.get("event_id", "")
        event = next((e for e in events if e.id == event_id), None)

        if event is None:
            message, is_error = "Please select an event.", True
        else:
            success, message = register_participant(event, name, email)
            is_error = not success

    return render_template(
        "index.html",
        events=events,
        message=message,
        is_error=is_error,
    )


if __name__ == "__main__":
    app.run(debug=True)
