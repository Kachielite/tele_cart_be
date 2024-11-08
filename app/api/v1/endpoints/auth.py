from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.core.dependency import db_dependency
from app.crud.crud_auth import create_business, auth_business, oauth2_bearer, get_current_business
from app.schemas.auth_schema import AuthRequestSchema, AuthResponseSchema, CurrentBusinessResponse
from app.schemas.general_response_schema import GeneralResponseSchema

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=GeneralResponseSchema)
async def create_new_business(db: db_dependency, business: AuthRequestSchema):
    code, response = create_business(business, db)
    if code != 201:
        raise HTTPException(status_code=code, detail=response["message"])
    return response


@router.post("/token", status_code=status.HTTP_200_OK, response_model=AuthResponseSchema)
async def authenticate_business(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    code, response = auth_business(form_data, db)
    if code != 200:
        raise HTTPException(status_code=code, detail=response["message"])
    return response


@router.get("/me", status_code=status.HTTP_200_OK, response_model=CurrentBusinessResponse)
async def current_business(token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency):
    code, response = get_current_business(token, db)
    if code != 200:
        raise HTTPException(status_code=code, detail=response["message"])
    return response