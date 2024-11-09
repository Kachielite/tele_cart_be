from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from app.core.dependency import auth_required, db_dependency
from app.crud.business import business_details, update_business, update_business_image
from app.schemas.business import BusinessResponseSchema, BusinessRequestSchema
from app.schemas.response import GeneralResponseSchema

router = APIRouter(prefix="/business", tags=["Manage Business"])

# Fetch business details
@router.get("/", status_code=200, response_model=BusinessResponseSchema, dependencies=[Depends(auth_required)])
async def get_business_details(db: db_dependency, business_id: int = Depends(auth_required)):
    code, response = business_details(business_id, db)
    if code != 200:
        raise HTTPException(status_code=code, detail=response["message"])
    return response


# Update business details
@router.put("/", status_code=200, response_model=GeneralResponseSchema, dependencies=[Depends(auth_required)])
async def update_business_details(business: BusinessRequestSchema, db: db_dependency, business_id: int = Depends(auth_required)):
    code, response = update_business(business_id, business, db)
    if code != 200:
        raise HTTPException(status_code=code, detail=response["message"])
    return response


# Update business image
@router.post("/image", status_code=200, response_model=GeneralResponseSchema, dependencies=[Depends(auth_required)])
async def update_business_profile_image(db: db_dependency, business_id: int = Depends(auth_required), image: UploadFile = File(...)):
    code, response = update_business_image(business_id, image, db)
    if code != 200:
        raise HTTPException(status_code=code, detail=response["message"])
    return response