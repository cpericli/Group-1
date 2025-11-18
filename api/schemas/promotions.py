from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
from decimal import Decimal

class PromotionBase(BaseModel):
    promotion_code: str
    description: Optional[str] = None
    discount_percentage: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    expiration_date: datetime
    is_active: Optional[int] = 1


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    promotion_code: Optional[str] = None
    description: Optional[str] = None
    discount_percentage: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    expiration_date: Optional[datetime] = None
    is_active: Optional[int] = None


class Promotion(PromotionBase):
    id: int

    class ConfigDict:
        from_attributes = True

class PromotionWithDiscount(BaseModel):
    promotion: Promotion
    original_price: Decimal
    discount_amount: Decimal
    final_price: Decimal