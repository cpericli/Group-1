from typing import Optional
from pydantic import BaseModel

class MenuBase(BaseModel):
    dish: str
    ingredients: str
    price: float
    calories: int
    food_category: str


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    dish: Optional[str] = None
    ingredients: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    food_category: Optional[str] = None


class Menu(MenuBase):
    id: int

    class ConfigDict:
        from_attributes = True