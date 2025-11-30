from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    genre = Column(String, unique=True, index=True, nullable=False)
    available_copies = Column(Integer, default=1)
    total_copies = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)


