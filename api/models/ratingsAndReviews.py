from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class RatingAndReview(Base):
    __tablename__ = "ratings_and_reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String(1000), nullable=False)
    rating = Column(Integer, nullable=False)
    
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)

    customer = relationship("Customer", back_populates="reviews")
    menu_item = relationship("MenuItems", back_populates="reviews")