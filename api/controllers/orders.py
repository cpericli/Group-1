from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from ..models import orders as order_model
from ..models import order_details as detail_model

def create(db: Session, request):
    new_order = order_model.Order(
        customer_id=request.customer_id,
        description=request.description,
        order_status=getattr(request, "order_status", None),
        promotion_id=getattr(request, "promotion_id", None),
    )

    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return new_order


def read_all(db: Session):
    try:
        result = db.query(order_model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return result


def read_one(db: Session, item_id: int):
    try:
        item = (
            db.query(order_model.Order)
            .filter(order_model.Order.id == item_id)
            .first()
        )
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order id not found!",
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return item


def update(db: Session, item_id: int, request):
    try:
        item_query = (
            db.query(order_model.Order)
            .filter(order_model.Order.id == item_id)
        )
        if not item_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order id not found!",
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



def delete(db: Session, item_id: int):
    try:
        item_query = (
            db.query(order_model.Order)
            .filter(order_model.Order.id == item_id)
        )
        if not item_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order id not found!",
            )
        item_query.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return {"detail": "Order deleted"}

def add_item_to_order(db: Session, order_id: int, request):
    # Ensure order exists
    order = (
        db.query(order_model.Order)
        .filter(order_model.Order.id == order_id)
        .first()
    )
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order id not found!",
        )

    new_detail = detail_model.OrderDetail(
        order_id=order_id,
        sandwich_id=request.sandwich_id,
        amount=request.amount,
    )

    try:
        db.add(new_detail)
        db.commit()
        db.refresh(new_detail)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return order


def get_customer_orders(db: Session, customer_id: int):
    try:
        result = (
            db.query(order_model.Order)
            .filter(order_model.Order.customer_id == customer_id)
            .order_by(order_model.Order.order_date.desc())
            .all()
        )
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return result


def place_order(db: Session, order_id: int):
    try:
        order_query = (
            db.query(order_model.Order)
            .filter(order_model.Order.id == order_id)
        )
        db_order = order_query.first()
        if not db_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order id not found!",
            )

        order_query.update({"order_status": "Completed"}, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return order_query.first()
