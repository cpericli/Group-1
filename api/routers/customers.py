from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..controllers import customers as controller
from ..schemas import customers as schema

router = APIRouter(
    tags=["Customers"],
    prefix="/customers"
)


# Browse Customer
@router.get("/", response_model=list[schema.Customer])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{customer_id}", response_model=schema.Customer)
def read_one(customer_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, customer_id=customer_id)


# Customize Customer details
@router.post("/", response_model=schema.Customer)
def create(request: schema.CustomerCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.put("/{customer_id}", response_model=schema.Customer)
def update(customer_id: int, request: schema.CustomerUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, customer_id=customer_id, request=request)


@router.delete("/{customer_id}")
def delete(customer_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, customer_id=customer_id)
