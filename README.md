# Event Registration System

## Project description
Event Registration System — іс-шараларға (семинарлар, конференциялар,
митаптар) қатысушыларды онлайн тіркеуді автоматтандыратын минималды веб-
қосымша. Қолданушы қолжетімді іс-шаралар тізімін көреді, аты-жөні мен email
арқылы тіркеледі, ал жүйе орындардың бос санын және қайталанған тіркеулерді
бақылайды.

## Users
- **Participant** — іс-шараларды қарап, тіркеу формасын толтырады.
- **Organizer / Admin** — іс-шаралар мен тіркелген қатысушылар тізімін
  қадағалайды.

## Main functions
1. Қолжетімді іс-шаралар тізімін көрсету (атауы, күні, бос орын саны).
2. Қатысушыны аты-жөні мен email арқылы іс-шараға тіркеу.
3. Енгізілген деректерді валидациялау (аты, email форматы).
4. Бір email-дың бір іс-шараға қайта тіркелуіне жол бермеу.
5. Орындар толғанда іс-шараны «FULL» деп белгілеп, тіркеуге тыйым салу.

Толық функционалдық талаптар тізімі: [`docs/requirements.md`](docs/requirements.md).

## Project structure
```
src/
  app.py                     # Flask application (routes)
  db.py                      # SQLite persistence layer (events + registrations)
  models.py                  # Pure validation logic (name/email)
  event_registration.db      # SQLite database file, created on first run
  templates/
    index.html               # Jinja2 page template
  static/
    style.css                 # Styling
docs/
  requirements.md            # Functional requirements
tests/
  test_models.py             # pytest unit tests for validation logic
  test_db.py                 # pytest tests for the SQLite registration flow
```

## Data storage
Data is stored in a local SQLite database (`src/event_registration.db`),
created automatically on first run. It persists across server restarts.
The database file is excluded from git via `.gitignore`.

## How to run
```bash
pip install -r requirements.txt
cd src
python app.py
# Open http://127.0.0.1:5000
```

## How to run tests
```bash
pip install -r requirements.txt
pytest tests/
```

## Author
Аты-жөні, тобы — [толтырыңыз].

## Technologies
- Python 3
- Flask
- Jinja2
- pytest
- HTML / CSS
