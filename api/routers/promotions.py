from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..controllers import promotions as controller
from ..schemas import promotions as schema

router = APIRouter(
    tags=["Promotions"],
    prefix="/promotions"
)

@router.post("/", response_model=schema.Promotion)
def create_promotion(promotion: schema.PromotionCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, promotion=promotion)

@router.get("/", response_model=list[schema.Promotion])
def read_all_promotions(db: Session = Depends(get_db)):
    return controller.read_all(db=db)

@router.get("/active", response_model=list[schema.Promotion])
def read_active_promotions(db: Session = Depends(get_db)):
    return controller.read_active(db=db)

@router.put("/{promotion_id}", response_model=schema.Promotion)
def update_promotion(promotion_id: int, promotion: schema.PromotionUpdate, db: Session = Depends(get_db)):
    db_promotion = controller.read_one(db=db, promotion_id=promotion_id)
    if not db_promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return controller.update(db=db, promotion_id=promotion_id, promotion=promotion)

@router.delete("/{promotion_id}", response_model=schema.Promotion)
def delete_promotion(promotion_id: int, db: Session = Depends(get_db)):
    promotion = controller.read_one(db=db, promotion_id=promotion_id)
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return controller.delete(db=db, promotion_id=promotion_id)


