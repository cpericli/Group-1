from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class PaymentInfo(Base):
    __tablename__ = "payment_infos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_number = Column(Integer, nullable=False)
    card_holder_name = Column(String(100), nullable=False)
    expiration_date = Column(String(100), nullable=False)
    cvv = Column(Integer, nullable=False)
    card_type = Column(String(100), nullable=False)

    status = Column(String(100), nullable=False, server_default="Not Completed")
