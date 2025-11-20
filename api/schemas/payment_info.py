from typing import Optional
from pydantic import BaseModel

class PaymentBase(BaseModel):
    card_last4: int
    card_holder_name: str
    expiration_date: str
    card_type: str


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    card_last4: Optional[str] = None
    card_holder_name: Optional[str] = None
    expiration_date: Optional[str] = None
    card_type: Optional[str] = None


class Payment(PaymentBase):
    id: int

    class ConfigDict:
        from_attributes = True