from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.security import decode_token
from app.crud.auth import get_current_business, oauth2_bearer
from app.db.session import get_db

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_business)]

async def auth_required(token: Annotated[str, Depends(oauth2_bearer)]) -> dict:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return decode_token(token).get("id")