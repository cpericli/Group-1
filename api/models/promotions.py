from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotion"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    promotion_code = Column(Integer, nullable=False)
    expiration_date = Column(DATETIME, nullable=False)
    
    orders = relationship("Order", back_populates="promotion")