from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Menu(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dish = Column(String(100), nullable=False)
    ingredients = Column(String(500), nullable=False)
    price = Column(DECIMAL(4,2), nullable=False)
    calories = Column(Integer, nullable=False)
    food_category = Column(String(100), nullable=False)

    