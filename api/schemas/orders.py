from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from decimal import Decimal
from .order_details import OrderDetail

class OrderBase(BaseModel):
    description: Optional[str] = None
    order_status: Optional[str] = None

class OrderCreate(OrderBase):
    customer_id: int

class OrderUpdate(BaseModel):
    description: Optional[str] = None
    order_status: Optional[str] = None
    promotion_id: Optional[int] = None

class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    customer_id: int
    promotion_id: Optional[int] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True

class OrderWithPricing(Order):
    """Extended order schema with pricing information"""
    total_price: Decimal
    discounted_total: Decimal
    discount_applied: Optional[Decimal] = None