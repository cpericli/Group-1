from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PromotionBase(BaseModel):
    promotion_code: int
    expiration_date: datetime


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    promotion_code: Optional[int] = None
    expiration_date: Optional[datetime] = None


class Promotion(PromotionBase):
    id: int

    class ConfigDict:
        from_attributes = True