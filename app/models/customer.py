from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, event

from app.db.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, index=True)
    name = Column(String)
    phone_number = Column(String, unique=True, index=True, nullable=True)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

@event.listens_for(Customer, "before_update")
def receive_before_update(mapper, connection, target):
    target.updated_at = datetime.now()