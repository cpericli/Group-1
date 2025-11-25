from fastapi import APIRouter, Depends, HTTPException, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema, order_details as order_detail_schema
from ..dependencies.database import engine, get_db
from datetime import date
from decimal import Decimal



router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.OrderPublic)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.get("/track/{order_id}", response_model=schema.Order)
def track_order(order_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, item_id=order_id)


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
    return db_order


@router.get("/customer/{customer_id}", response_model=list[schema.OrderWithPricing])
def get_order_history(customer_id: int, db: Session = Depends(get_db)):
    orders = controller.get_customer_orders(db=db, customer_id=customer_id)

    result: list[schema.OrderWithPricing] = []
    for o in orders:
        order_with_pricing = schema.OrderWithPricing.model_validate(o, from_attributes=True)

        # Calculate pricing (add your logic here)
        order_with_pricing.total_price = Decimal("0.00")  # Your calculation
        order_with_pricing.discounted_total = Decimal("0.00")  # Your calculation
        order_with_pricing.discount_applied = None  # Your calculation

        result.append(order_with_pricing)

    return result

@router.get("/by-date/", response_model=list[schema.Order])
def read_orders_by_date(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
):
    return controller.read_by_date_range(db=db, start_date=start_date, end_date=end_date)

@router.get("/revenue/day", response_model=schema.DailyRevenue)
def get_daily_revenue(
    day: date,
    db: Session = Depends(get_db),
):
    total = controller.get_daily_revenue(db=db, day=day)
    return schema.DailyRevenue(date=day, total_revenue=total)