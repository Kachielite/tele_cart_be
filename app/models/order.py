from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, event, Float

from app.db.base import Base
from app.enums.order_status import OrderStatus


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customers_id = Column(Integer, ForeignKey("customers.id"), index=True)
    businesses_id = Column(Integer, ForeignKey("businesses.id"), index=True)
    status = Column(Enum(OrderStatus), index=True, default=OrderStatus.pending)
    total = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


@event.listens_for(Order, "before_update")
def receive_before_update(mapper, connection, target):
    target.updated_at = datetime.now()