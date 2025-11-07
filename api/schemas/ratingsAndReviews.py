from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from ..models.menuItems import MenuItems # MenuItem
from ..models.customers import Customer


class RatingAndReviewBase(BaseModel):
    text: str
    rating: int


class RatingAndReviewCreate(RatingAndReviewBase):
    customer_id: int
    menu_item_id: int


class RatingAndReviewUpdate(BaseModel):
    text: Optional[str] = None
    rating: Optional[int] = None
    customer_id: Optional[int] = None
    menu_item_id: Optional[int] = None


class RatingAndReview(RatingAndReviewBase):
    id: int
    customer_id: int
    menu_item_id: int
    customer: Optional[Customer] = None
    menu_item: Optional[MenuItems] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
