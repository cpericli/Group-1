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
    @property
    def discounted_total(self):
        """Calculate total price after applying promotion discount"""
        base_total = self.total_price

        if not self.promotion:
            return base_total

        if self.promotion.expiration_date < datetime.now():
            return base_total

        if not self.promotion.is_active:
            return base_total

        if self.promotion.discount_percentage:
            discount = base_total * (self.promotion.discount_percentage / 100)
            return base_total - discount

        if self.promotion.discount_amount:
            return max(0, base_total - self.promotion.discount_amount)

        return base_total