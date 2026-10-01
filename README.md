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
  app.py            # Flask application (routes)
  models.py         # Pure data logic: Event, validation, registration
  templates/
    index.html      # Jinja2 page template
  static/
    style.css        # Styling
docs/
  requirements.md   # Functional requirements
tests/
  test_models.py    # pytest unit tests for validation/registration logic
```

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
