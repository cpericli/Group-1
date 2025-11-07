from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100))
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))
    order_status = Column(String(100), nullable=False, server_default="Not completed")
    order_details = relationship("OrderDetail", back_populates="order")

    @property
    def total_price(self):
        """Calculate total price from all order details"""
        return sum(
            detail.amount * detail.sandwich.price 
            for detail in self.order_details
        )