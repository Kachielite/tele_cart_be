from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime

from app.db.base import Base


class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    added_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)