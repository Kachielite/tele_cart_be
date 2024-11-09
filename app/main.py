import logging.config

from fastapi import FastAPI

from app.api.v1.endpoints import auth, health, business
from app.db.base import Base
from app.db.session import engine
from app.core.log_config import LOGGING_CONFIG  # Import the logger configuration

# Configure the logger
logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)

app = FastAPI()
Base.metadata.create_all(engine)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(business.router)
