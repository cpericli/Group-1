from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from ..models import customers as model


def create(db: Session, request):
    new_item = model.Customer(
        name=request.name,
        email=request.email,
        phone=request.phone,
        address=request.address
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Customer).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return result


def read_one(db: Session, customer_id: int):
    try:
        item = (
            db.query(model.Customer)
            .filter(model.Customer.id == customer_id)
            .first()
        )
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer id not found!",
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return item


def update(db: Session, customer_id: int, request):
    try:
        item_query = (
            db.query(model.Customer)
            .filter(model.Customer.id == customer_id)
        )
        if not item_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer id not found!",
            )

        update_data = request.dict(exclude_unset=True)
        item_query.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return item_query.first()


def delete(db: Session, customer_id: int):
    try:
        item_query = (
            db.query(model.Customer)
            .filter(model.Customer.id == customer_id)
        )
        if not item_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer id not found!",
            )
        item_query.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return {"detail": "Customer deleted"}
