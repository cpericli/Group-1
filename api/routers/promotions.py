from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..controllers import promotions as controller
from ..schemas import promotions as schema

router = APIRouter(
    tags=["Promotions"],
    prefix="/promotions"
)

@router.get("/", response_model=list[schema.Promotion])
def read_all_promotions(db: Session = Depends(get_db)):
    """Get all promotions"""
    return controller.read_all(db=db)

@router.get("/active", response_model=list[schema.Promotion])
def read_active_promotions(db: Session = Depends(get_db)):
    """Get all active and non-expired promotions"""
    return controller.read_active(db=db)

@router.get("/{promotion_id}", response_model=schema.Promotion)
def read_one_promotion(promotion_id: int, db: Session = Depends(get_db)):
    """Get a specific promotion"""
    promotion = controller.read_one(db=db, promotion_id=promotion_id)
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promotion

@router.get("/code/{promotion_code}", response_model=schema.Promotion)
def read_promotion_by_code(promotion_code: str, db: Session = Depends(get_db)):
    """Get a promotion by its code"""
    promotion = controller.read_by_code(db=db, promotion_code=promotion_code)
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion code not found")
    return promotion

@router.post("/apply/{order_id}/{promotion_id}")
def apply_promotion(order_id: int, promotion_id: int, db: Session = Depends(get_db)):
    """Apply a promotion to an order"""
    return controller.apply_promotion_to_order(db=db, order_id=order_id, promotion_id=promotion_id)

@router.delete("/remove/{order_id}")
def remove_promotion(order_id: int, db: Session = Depends(get_db)):
    """Remove promotion from an order"""
    return controller.remove_promotion_from_order(db=db, order_id=order_id)

