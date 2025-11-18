from typing import Optional
from pydantic import BaseModel

class RatingBase(BaseModel):
    text: str
    rating: int
    customer_id: int
    menu_item_id: int


class RatingCreate(RatingBase):
    customer_id: int
    menu_item_id: int


class RatingUpdate(BaseModel):
    text: Optional[str] = None
    rating: Optional[int] = None
    customer_id: Optional[int] = None
    menu_item_id: Optional[int] = None


class Rating(RatingBase):
    id: int

    class ConfigDict:
        from_attributes = True
