from fastapi import APIRouter, Depends, HTTPException, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema, order_details as order_detail_schema
from ..dependencies.database import engine, get_db


router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)


@router.post("/{order_id}/items", response_model=schema.Order)
def add_to_cart(order_id: int, request: order_detail_schema.OrderDetailCreate, db: Session = Depends(get_db)):
    updated_order = controller.add_item_to_order(db=db, order_id=order_id, request=request)
    return updated_order


@router.post("/{order_id}/place", response_model=schema.OrderWithPricing)
def place_order(order_id: int, db: Session = Depends(get_db)):
    db_order = controller.place_order(db=db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return schema.OrderWithPricing(
        id=db_order.id,
        description=db_order.description,
        order_status=db_order.order_status,
        order_date=db_order.order_date,
        customer_id=db_order.customer_id,
        promotion_id=db_order.promotion_id,
        order_details=db_order.order_details,
        total_price=db_order.total_price,
        discounted_total=db_order.discounted_total,
        discount_applied=(
            db_order.total_price - db_order.discounted_total
            if db_order.total_price != db_order.discounted_total
            else None
        ),
    )
