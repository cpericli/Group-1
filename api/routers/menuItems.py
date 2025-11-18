from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..controllers import menuItems as controller
from ..schemas import menu as schema

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
