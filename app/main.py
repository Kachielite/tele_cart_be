import logging.config

from fastapi import FastAPI

from app.telebot.bot import main as telegram_bot_main
from app.api.v1.endpoints import auth, health, business, category, product, order
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
app.include_router(category.router)
app.include_router(product.router)
app.include_router(order.router)

telegram_bot_main()


