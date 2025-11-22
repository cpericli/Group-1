from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from ..models import orders as order_model
from ..models import order_details as detail_model

def create(db: Session, request):
    order_status = request.order_status or "Not completed"

    new_order = order_model.Order(
        customer_id=request.customer_id,
        description=request.description,
        order_status="Not completed",
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

def place_order(db: Session, order_id: int):
    db_order = db.query(order_model.Order).filter(order_model.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order id not found!")

    order_details = db_order.order_details
    if not order_details:
        raise HTTPException(status_code=400, detail="Order has no items.")

    for detail in order_details:
        sandwich = detail.sandwich
        for recipe in sandwich.recipes:
            resource = recipe.resource
            required_amount = recipe.amount * detail.amount

            if resource.amount < required_amount:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient {resource.item}. Need {required_amount}, have {resource.amount}."
                )

    for detail in order_details:
        sandwich = detail.sandwich
        for recipe in sandwich.recipes:
            resource = recipe.resource
            required_amount = recipe.amount * detail.amount
            resource.amount -= required_amount

    db_order.order_status = "Completed"
    db.commit()
    db.refresh(db_order)

    return db_order


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


