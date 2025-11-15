from typing import Optional
from pydantic import BaseModel

class RatingBase(BaseModel):
    id: int
    text: str
    rating: int


class RatingCreate(RatingBase):
    pass


class RatingUpdate(BaseModel):
    id: int
    text: Optional[str] = None
    rating: Optional[int] = None


class Rating(RatingBase):
    id: int

    class ConfigDict:
        from_attributes = True
