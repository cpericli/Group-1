from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..schemas.menu import Menu, MenuCreate, MenuUpdate
from ..controllers import menu as menu_controller

router = APIRouter(
    prefix="/menu",
    tags=["Menu"],
)


@router.get("/", response_model=List[Menu])
def browse_menu(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Browse all menu items.
    """
    return menu_controller.read_all(db=db, skip=skip, limit=limit)


@router.get("/{menu_id}", response_model=Menu)
def get_menu_item(menu_id: int, db: Session = Depends(get_db)):
    """
    Get a single menu item by id.
    """
    item = menu_controller.read_one(db=db, menu_id=menu_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item


@router.post("/", response_model=Menu, status_code=201)
def create_menu_item(menu: MenuCreate, db: Session = Depends(get_db)):
    """
    Create a new menu item.
    (Useful for staff / customization of available menu items.)
    """
    return menu_controller.create(db=db, menu=menu)


@router.put("/{menu_id}", response_model=Menu)
def update_menu_item(menu_id: int, menu: MenuUpdate, db: Session = Depends(get_db)):
    """
    Update an existing menu item.
    This supports the 'Customize Menu Items' user story.
    """
    updated = menu_controller.update(db=db, menu_id=menu_id, menu=menu)
    if updated is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return updated


@router.delete("/{menu_id}", response_model=Menu)
def delete_menu_item(menu_id: int, db: Session = Depends(get_db)):
    """
    Delete a menu item.
    """
    deleted = menu_controller.delete(db=db, menu_id=menu_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return deleted
