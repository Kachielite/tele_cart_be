from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, event, Float

from app.db.base import Base
from app.enums.order_status import OrderStatus


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), index=True)
    business_id = Column(Integer, ForeignKey("business.id"), index=True)
    status = Column(Enum(OrderStatus), index=True, default=OrderStatus.PENDING)
    total = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


@event.listens_for(Order, "before_update")
def receive_before_update(mapper, connection, target):
    target.updated_at = datetime.now()