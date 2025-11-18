from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    promotion_code = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    discount_percentage = Column(DECIMAL(5, 2), nullable=True)
    discount_amount = Column(DECIMAL(10, 2), nullable=True)
    expiration_date = Column(DATETIME, nullable=False)
    is_active = Column(Integer, default=1)
    
    orders = relationship("Order", back_populates="promotion")