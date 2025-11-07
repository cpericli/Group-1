from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    description = Column(String(300))
    order_status = Column(String(100), nullable=False, server_default="Not completed")
    order_details = relationship("OrderDetail", back_populates="order")
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", back_populates="orders")

    promotion_id = Column(Integer, ForeignKey("promotions.id"), nullable=True)
    promotion = relationship("Promotion", back_populates="orders")
    @property
    def total_price(self):
        """Calculate total price from all order details"""
        return sum(
            detail.amount * detail.sandwich.price 
            for detail in self.order_details
        )