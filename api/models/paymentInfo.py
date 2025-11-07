from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class PaymentInfo(Base):
    __tablename__ = "payment_infos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_last4 = Column(Integer, nullable=False)
    card_holder_name = Column(String(100), nullable=False)
    expiration_date = Column(String(100), nullable=False)
    card_type = Column(String(100), nullable=False)

    status = Column(String(100), nullable=False, server_default="Not Completed")

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    order = relationship("Order", back_populates="payment")