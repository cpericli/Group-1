from sqlalchemy.orm import Session
from datetime import datetime
from ..models.promotions import Promotion
from ..models.orders import Order
from ..schemas.promotions import PromotionCreate, PromotionUpdate
from fastapi import HTTPException
from decimal import Decimal

def create(db: Session, promotion: PromotionCreate):
    """Create a new promotion"""
    db_promotion = Promotion(**promotion.model_dump())
    db.add(db_promotion)
    db.commit()
    db.refresh(db_promotion)
    return db_promotion

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

def update(db: Session, promotion_id: int, promotion: PromotionUpdate):
    """Update a promotion"""
    db_promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    if db_promotion:
        update_data = promotion.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_promotion, key, value)
        db.commit()
        db.refresh(db_promotion)
    return db_promotion

def delete(db: Session, promotion_id: int):
    """Delete a promotion"""
    db_promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    if db_promotion:
        db.delete(db_promotion)
        db.commit()
    return db_promotion
