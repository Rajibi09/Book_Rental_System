from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models.book import Book


router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=schemas.BookInDB, status_code=status.HTTP_201_CREATED)
def create_book(book_in: schemas.BookCreate, db: Session = Depends(get_db)):
    if db.query(Book).filter(Book.genre == book_in.genre).first():
        raise HTTPException(status_code=400, detail="Book with this genre already exists")

    available_copies = (
        book_in.available_copies if book_in.available_copies is not None else book_in.total_copies
    )

    db_book = Book(
        title=book_in.title,
        author=book_in.author,
        genre=book_in.genre,
        total_copies=book_in.total_copies,
        available_copies=available_copies,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/", response_model=list[schemas.BookInDB])
def list_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(Book).offset(skip).limit(limit).all()
    return books


@router.get("/{book_id}", response_model=schemas.BookInDB)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.patch("/{book_id}", response_model=schemas.BookInDB)
def update_book(book_id: int, book_in: schemas.BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return None


