from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, event

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, nullable=False)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    businesses_id = Column(Integer, ForeignKey("businesses.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

@event.listens_for(Product, "before_update")
def receive_before_update(mapper, connection, target):
    target.updated_at = datetime.now()
