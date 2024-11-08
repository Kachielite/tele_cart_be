from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, event, Boolean

from app.db.base import Base


class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True, index=True, nullable=False)
    business_name = Column(String, index=True)
    description = Column(String)
    address = Column(String)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

@event.listens_for(Business, "before_update")
def receive_before_update(mapper, connection, target):
    target.updated_at = datetime.now()