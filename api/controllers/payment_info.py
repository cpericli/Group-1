from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from ..models.payment_info import PaymentInfo as PaymentInfoModel
from ..schemas.payment_info import PaymentCreate, PaymentUpdate


def create(db: Session, payment: PaymentCreate, order_id: int):
    new_payment = PaymentInfoModel(
        card_last4=payment.card_last4,
        card_holder_name=payment.card_holder_name,
        expiration_date=payment.expiration_date,
        card_type=payment.card_type,
        order_id=order_id
    )

    try:
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )

    return new_payment


def read_all(db: Session):
    try:
        return db.query(PaymentInfoModel).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )


def read_one(db: Session, payment_id: int):
    try:
        payment = db.query(PaymentInfoModel).filter(PaymentInfoModel.id == payment_id).first()
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment info not found"
            )
        return payment

    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )


def update(db: Session, payment_id: int, update_data: PaymentUpdate):
    try:
        payment = db.query(PaymentInfoModel).filter(PaymentInfoModel.id == payment_id)

        if not payment.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment info not found"
            )

        update_fields = update_data.dict(exclude_unset=True)
        payment.update(update_fields, synchronize_session=False)
        db.commit()

        return payment.first()

    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )


def delete(db: Session, payment_id: int):
    try:
        payment = db.query(PaymentInfoModel).filter(PaymentInfoModel.id == payment_id)

        if not payment.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment info not found"
            )

        payment.delete(synchronize_session=False)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )

    return {"message": "Payment info deleted successfully"}
