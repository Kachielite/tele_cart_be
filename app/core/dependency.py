from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud.crud_auth import get_current_business
from app.db.session import get_db

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_business)]