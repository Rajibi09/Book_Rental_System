from datetime import datetime

from pydantic import BaseModel


class RentalBase(BaseModel):
    user_id: int
    book_id: int


class RentalCreate(RentalBase):
    pass


class RentalReturn(BaseModel):
    returned_at: datetime | None = None


class RentalInDB(RentalBase):
    id: int
    rented_at: datetime
    returned_at: datetime | None
    is_active: bool

    class Config:
        from_attributes = True


