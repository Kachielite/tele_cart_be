from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, event

from app.db.base import Base


class OrderItems(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    orders_id = Column(Integer, ForeignKey('orders.id'))
    products_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

@event.listens_for(OrderItems, "before_update")
def receive_before_update(mapper, connection, target):
    target.updated_at = datetime.now()


