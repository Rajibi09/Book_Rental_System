from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    total_copies: int = 1


class BookCreate(BookBase):
    available_copies: int | None = None


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    total_copies: int | None = None
    available_copies: int | None = None


class BookInDB(BookBase):
    id: int
    available_copies: int
    is_active: bool

    class Config:
        from_attributes = True


