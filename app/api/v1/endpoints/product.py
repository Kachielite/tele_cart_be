from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from app.core.dependency import auth_required, db_dependency
from app.crud.product import create_product, add_product_image, read_product, read_all_products, remove_product
from app.schemas.product import ProductCreationRequest, ProductResponse
from app.schemas.response import GeneralResponseSchema

router = APIRouter(prefix='/v1/products', tags=['Manage Products'])

@router.get('/{business_identifier}', status_code=200, response_model=List[ProductResponse])
async def get_all_products(db: db_dependency, business_identifier: str):
    code, response = read_all_products(db, business_identifier)
    if code != 200:
        raise HTTPException(status_code=code, detail=response["message"])
    return response


@router.post('/', status_code=201, response_model=GeneralResponseSchema, dependencies=[Depends(auth_required)])
async def create_new_product(db: db_dependency, product: ProductCreationRequest, business_id: int = Depends(auth_required)):
    code, response = create_product(db, product, business_id)
    if code != 201:
        raise HTTPException(status_code=code, detail=response["message"])
    return response


@router.post('/{product_id}/image', status_code=200, response_model=GeneralResponseSchema, dependencies=[Depends(auth_required)])
async def upload_product_image(db: db_dependency, product_id: int, image: UploadFile = File(...), business_id: int = Depends(auth_required)):
    code, response = add_product_image(db, product_id, image, business_id)
    if code != 200:
        raise HTTPException(status_code=code, detail=response["message"])
    return response


@router.get('/details/{business_identifier}', status_code=200, response_model=ProductResponse)
async def get_product_details(db: db_dependency, product_id: int, business_identifier: str):
    code, response = read_product(db, product_id, business_identifier)
    if code != 200:
        raise HTTPException(status_code=code, detail=response["message"])
    return response

@router.delete('/{product_id}', status_code=200, response_model=GeneralResponseSchema, dependencies=[Depends(auth_required)])
async def delete_product(db: db_dependency, product_id: int, business_id: int = Depends(auth_required)):
    code, response = remove_product(db, product_id, business_id)
    if code != 200:
        raise HTTPException(status_code=code, detail=response["message"])
    return response


