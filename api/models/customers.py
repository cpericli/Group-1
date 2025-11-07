from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=False, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(100), unique=True, nullable=False)
    address = Column(String(100), unique=True, nullable=False)

    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    reviews = relationship("RatingAndReview", back_populates="customer", cascade="all, delete-orphan")

    


    
