from sqlalchemy.orm import Session
from datetime import datetime
from ..models.promotions import Promotion
from ..models.orders import Order
from ..schemas.promotions import PromotionCreate, PromotionUpdate
from fastapi import HTTPException
from decimal import Decimal

def create(db: Session, promotion: PromotionCreate):
    db_promotion = Promotion(**promotion.model_dump())
    db.add(db_promotion)
    db.commit()
    db.refresh(db_promotion)
    return db_promotion

def read_all(db: Session):
    return db.query(Promotion).all()


def read_one(db: Session, promotion_id: int):
    db_promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    if not db_promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return db_promotion

def read_active(db: Session):
    current_time = datetime.now()
    return db.query(Promotion).filter(
        Promotion.is_active == 1,
        Promotion.expiration_date > current_time
    ).all()

def update(db: Session, promotion_id: int, promotion: PromotionUpdate):
    db_promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    if db_promotion:
        update_data = promotion.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_promotion, key, value)
        db.commit()
        db.refresh(db_promotion)
    return db_promotion

def delete(db: Session, promotion_id: int):
    db_promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    if db_promotion:
        db.delete(db_promotion)
        db.commit()
    return db_promotion

