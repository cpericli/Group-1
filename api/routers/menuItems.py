from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..controllers import menuItems as controller
from ..schemas import menu as schema
from typing import Optional
from fastapi import Query


router = APIRouter(
    tags=["Menu"],
    prefix="/menu"
)


# Browse Menu
@router.get("/", response_model=list[schema.Menu])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Menu)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


# Customize Menu Items (admin/staff use)
@router.post("/", response_model=schema.Menu)
def create(request: schema.MenuCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.put("/{item_id}", response_model=schema.Menu)
def update(item_id: int, request: schema.MenuUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, item_id=item_id, request=request)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

@router.get("/search", response_model=list[schema.Menu])
def search_menu_items(
    q: Optional[str] = Query(
        default=None,
        description="Free-text search in dish name or ingredients."
    ),
    category: Optional[str] = Query(
        default=None,
        description="Filter by food_category (e.g., 'vegetarian', 'vegan', 'dessert')."
    ),
    db: Session = Depends(get_db),
):

    items = controller.read_all(db=db)

    if q:
        q_lower = q.lower()
        items = [
            item for item in items
            if q_lower in (item.dish or "").lower()
            or q_lower in (item.ingredients or "").lower()
        ]

    if category:
        cat_lower = category.lower()
        items = [
            item for item in items
            if cat_lower in (item.food_category or "").lower()
        ]

    return items
