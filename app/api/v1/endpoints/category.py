from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.core.dependency import auth_required, db_dependency
from app.crud.category import fetch_categories, fetch_category_by_id
from app.schemas.category import CategoryResponse

router = APIRouter(prefix="/v1/category", tags=["Category"])

# Read all categories
@router.get("/", status_code=200, response_model=List[CategoryResponse], dependencies=[Depends(auth_required)])
async def read_categories(db: db_dependency):
    code, response = fetch_categories(db)
    if code != 200:
        raise HTTPException(status_code=code, detail=response["message"])
    return response


# Read category by id
@router.get("/{category_id}", status_code=200, response_model=CategoryResponse, dependencies=[Depends(auth_required)])
async def read_category_by_id(category_id: int, db: db_dependency):
    code, response = fetch_category_by_id(category_id, db)
    if code != 200:
        raise HTTPException(status_code=code, detail=response["message"])
    return response