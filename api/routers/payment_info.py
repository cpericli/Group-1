from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..controllers import payment_info as controller
from ..schemas import payment_info as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['PaymentInfo'],
    prefix="/payment_info"
)

# Create payment info for a specific order
@router.post("/{order_id}", response_model=schema.Payment)
def create_payment(order_id: int, request: schema.PaymentCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, payment=request, order_id=order_id)

# Get all payment records
@router.get("/", response_model=list[schema.Payment])
def read_all_payments(db: Session = Depends(get_db)):
    return controller.read_all(db)

# Get payment info by payment ID
@router.get("/{payment_id}", response_model=schema.Payment)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = controller.read_one(db, payment_id=payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

# Update payment info
@router.put("/{payment_id}", response_model=schema.Payment)
def update_payment(payment_id: int, request: schema.PaymentUpdate, db: Session = Depends(get_db)):
    updated_payment = controller.update(db, payment_id, request)
    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated_payment

# Delete payment info
@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    success = controller.delete(db, payment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"detail": "Payment deleted successfully"}
