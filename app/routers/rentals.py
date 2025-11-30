from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models.book import Book
from app.models.rental import Rental
from app.models.user import User


router = APIRouter(prefix="/rentals", tags=["rentals"])


@router.post("/", response_model=schemas.RentalInDB, status_code=status.HTTP_201_CREATED)
def create_rental(rental_in: schemas.RentalCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == rental_in.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    book = db.query(Book).filter(Book.id == rental_in.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="No available copies for this book")

    rental = Rental(
        user_id=rental_in.user_id,
        book_id=rental_in.book_id,
    )

    book.available_copies -= 1
    db.add(rental)
    db.commit()
    db.refresh(rental)
    return rental


@router.post("/{rental_id}/return", response_model=schemas.RentalInDB)
def return_rental(
    rental_id: int,
    rental_return: schemas.RentalReturn | None = None,
    db: Session = Depends(get_db),
):
    rental = db.query(Rental).filter(Rental.id == rental_id).first()
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")

    if rental.returned_at is not None:
        raise HTTPException(status_code=400, detail="Rental already returned")

    book = db.query(Book).filter(Book.id == rental.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    rental.returned_at = (
        rental_return.returned_at if rental_return and rental_return.returned_at else datetime.utcnow()
    )
    rental.is_active = False
    book.available_copies += 1

    db.commit()
    db.refresh(rental)
    return rental


@router.get("/", response_model=list[schemas.RentalInDB])
def list_rentals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rentals = db.query(Rental).offset(skip).limit(limit).all()
    return rentals


@router.get("/{rental_id}", response_model=schemas.RentalInDB)
def get_rental(rental_id: int, db: Session = Depends(get_db)):
    rental = db.query(Rental).filter(Rental.id == rental_id).first()
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental


