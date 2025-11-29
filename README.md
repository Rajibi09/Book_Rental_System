## Book Rental System (FastAPI, Python)

This is a simple **Book Rental System** built with **FastAPI** and **SQLAlchemy**.  
The code is split by responsibility:

- `database` configuration
- `models` (database tables)
- `schemas` (Pydantic models)
- `routers` (API endpoints)

### Project Structure

- `app/database.py` – database URL, engine, session, `get_db` dependency
- `app/models/` – `book.py`, `user.py`, `rental.py`
- `app/schemas/` – Pydantic models for requests/responses
- `app/routers/` – FastAPI routers for books, users, rentals
- `app/main.py` – FastAPI application entry point

### Install dependencies

From the `book_rental_fastapi` folder:

```bash
pip install -r requirements.txt
```

### Run the API

From the `book_rental_fastapi` folder:

```bash
uvicorn app.main:app --reload
```

Then open the automatic docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Main Endpoints

- `POST /users/` – create user
- `GET /users/` – list users
- `POST /books/` – add book
- `GET /books/` – list books
- `POST /rentals/` – create rental (decrease book copies)
- `POST /rentals/{id}/return` – return a book (increase book copies)


