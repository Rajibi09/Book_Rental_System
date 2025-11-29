from fastapi import FastAPI

from app.database import Base, engine
from app.models import author as author_model  # noqa: F401
from app.models import book as book_model  # noqa: F401
from app.models import category as category_model  # noqa: F401
from app.models import rental as rental_model  # noqa: F401
from app.models import user as user_model  # noqa: F401
from app.routers import books, rentals, users


def create_app() -> FastAPI:
    # Create database tables
    Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title="Book Rental System API",
        version="1.0.0",
        description="Simple FastAPI-based book rental system",
    )

    # Simple root endpoint so visiting "/" is not 404
    @app.get("/", tags=["root"])
    def read_root():
        return {
            "message": "Book Rental System API is running. Open /docs for the interactive UI."
        }

    # Routers
    app.include_router(users.router)
    app.include_router(books.router)
    app.include_router(rentals.router)

    return app


app = create_app()


