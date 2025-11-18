from sqlalchemy.orm import Session
from datetime import datetime
from ..models.promotions import Promotion
from ..models.orders import Order
from ..schemas.promotions import PromotionCreate, PromotionUpdate
from fastapi import HTTPException
from decimal import Decimal



def read_all(db: Session):
    """Get all promotions"""
    return db.query(Promotion).all()


def read_active(db: Session):
    """Get all active and non-expired promotions"""
    current_time = datetime.now()
    return db.query(Promotion).filter(
        Promotion.is_active == 1,
        Promotion.expiration_date > current_time
    ).all()


def read_one(db: Session, promotion_id: int):
    """Get a specific promotion by ID"""
    return db.query(Promotion).filter(Promotion.id == promotion_id).first()


def read_by_code(db: Session, promotion_code: str):
    """Get a promotion by its code"""
    return db.query(Promotion).filter(Promotion.promotion_code == promotion_code).first()


def validate_promotion(db: Session, promotion_id: int) -> tuple[bool, str]:
    """
    Validate if a promotion can be applied
    Returns: (is_valid, error_message)
    """
    promotion = read_one(db, promotion_id)

    if not promotion:
        return False, "Promotion not found"

    if not promotion.is_active:
        return False, "Promotion is no longer active"

    if promotion.expiration_date < datetime.now():
        return False, "Promotion has expired"

    if not promotion.discount_percentage and not promotion.discount_amount:
        return False, "Promotion has no discount configured"

    return True, "Promotion is valid"


def apply_promotion_to_order(db: Session, order_id: int, promotion_id: int):
    """
    Apply a promotion to an order
    Returns the updated order with discount information
    """
    # Get the order
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Validate the promotion
    is_valid, error_msg = validate_promotion(db, promotion_id)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    # Get the promotion
    promotion = read_one(db, promotion_id)

    # Apply promotion to order
    order.promotion_id = promotion_id
    db.commit()
    db.refresh(order)

    # Calculate discount
    original_price = order.total_price
    final_price = order.discounted_total
    discount = original_price - final_price

    return {
        "order_id": order.id,
        "promotion_code": promotion.promotion_code,
        "promotion_description": promotion.description,
        "original_price": float(original_price),
        "discount_amount": float(discount),
        "final_price": float(final_price)
    }


def remove_promotion_from_order(db: Session, order_id: int):
    """Remove a promotion from an order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.promotion_id = None
    db.commit()
    db.refresh(order)
    return order