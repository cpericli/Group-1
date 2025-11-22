from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal
from .order_details import OrderDetail


class OrderCreate(BaseModel):
    description: Optional[str] = Field(
        default=None,
        title="Delivery / Takeout / Dine-In",
        description="Specify how you'd like to receive your order (e.g. 'Delivery', 'Takeout', or 'Dine-In')."
    )
    customer_id: int
    promotion_id: Optional[int] = None


class OrderUpdate(BaseModel):
    description: Optional[str] = None
    order_status: Optional[str] = None
    promotion_id: Optional[int] = None


class Order(BaseModel):
    id: int
    order_date: Optional[datetime] = None
    order_type: Optional[str] = Field(
        default=None,
        alias="description",
        title="Dine-in / Takeout / Delivery",
        description="How the order will be received."
    )
    order_status: str
    customer_id: int
    promotion_id: Optional[int] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True
        populate_by_name = True


class OrderPublic(BaseModel):
    id: int
    order_date: Optional[datetime] = None

    order_type: Optional[str] = Field(
        default=None,
        alias="description",
        title="Dine-in / Takeout / Delivery",
        description="How the order will be received."
    )

    customer_id: int
    promotion_id: Optional[int] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True
        populate_by_name = True


class OrderWithPricing(Order):
    total_price: Decimal
    discounted_total: Decimal
    discount_applied: Optional[Decimal] = None