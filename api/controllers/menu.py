from typing import List, Optional
from sqlalchemy.orm import Session

from ..models.menuItems import MenuItems
from ..schemas.menu import MenuCreate, MenuUpdate


def create(db: Session, menu: MenuCreate) -> MenuItems:
    db_item = MenuItems(**menu.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def read_all(db: Session, skip: int = 0, limit: int = 100) -> List[MenuItems]:
    return (
        db.query(MenuItems)
        .offset(skip)
        .limit(limit)
        .all()
    )


def read_one(db: Session, menu_id: int) -> Optional[MenuItems]:
    return (
        db.query(MenuItems)
        .filter(MenuItems.id == menu_id)
        .first()
    )


def update(db: Session, menu_id: int, menu: MenuUpdate) -> Optional[MenuItems]:
    db_item = read_one(db, menu_id)
    if db_item is None:
        return None

    update_data = menu.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete(db: Session, menu_id: int) -> Optional[MenuItems]:
    db_item = read_one(db, menu_id)
    if db_item is None:
        return None

    db.delete(db_item)
    db.commit()
    return db_item
