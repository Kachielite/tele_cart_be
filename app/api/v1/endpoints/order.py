from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.core.dependency import auth_required, db_dependency
from app.crud.order import fetch_orders, fetch_order_by_id, update_order_status, fetch_customer_orders, create_order
from app.enums.order_status import OrderStatus
from app.schemas.order import OrderResponse, OrderRequest
from app.schemas.response import GeneralResponseSchema

router = APIRouter(prefix="/v1/order", tags=["Manage Orders"])

# Create new order
@router.post("/", status_code=201, response_model=GeneralResponseSchema, dependencies=[Depends(auth_required)])
async def create_new_order(db: db_dependency, order: OrderRequest, business_id: int = Depends(auth_required)):
    code, response = create_order(db, business_id, order)
    if code != 201:
        raise HTTPException(status_code=code, detail=response["message"])
    return response

# Fetch all orders
@router.get("/", status_code=200, response_model=List[OrderResponse], dependencies=[Depends(auth_required)])
async def get_all_orders(db: db_dependency, page: int = 1, page_size: int = 10, business_id: int = Depends(auth_required)):
    code, response = fetch_orders(db, business_id, page, page_size)
    if code != 200:
        raise HTTPException(status_code=code, detail=response["message"])
    return response

# Fetch order by id
@router.get("/{order_id}", status_code=200, response_model=OrderResponse, dependencies=[Depends(auth_required)])
async def get_order_by_id(db: db_dependency, order_id: int, business_id: int = Depends(auth_required)):
    code, response = fetch_order_by_id(db, order_id, business_id)
    if code != 200:
        raise HTTPException(status_code=code, detail=response["message"])
    return response

# Update order status
@router.put("/{order_id}/status", status_code=200, response_model=GeneralResponseSchema, dependencies=[Depends(auth_required)])
async def update_status_of_order(db: db_dependency, order_id: int, status: OrderStatus, business_id: int = Depends(auth_required)):
    code, response = update_order_status(db, order_id, status, business_id)
    if code != 200:
        raise HTTPException(status_code=code, detail=response["message"])
    return response


# Retrieve Customer Orders
@router.get("/customer/{customer_id}", status_code=200, response_model=List[OrderResponse], dependencies=[Depends(auth_required)])
async def get_customer_orders(db: db_dependency, customer_id: int, page: int = 1, page_size: int = 10, business_id: int = Depends(auth_required)):
    code, response = fetch_customer_orders(db, customer_id, business_id, page, page_size,)
    if code != 200:
        raise HTTPException(status_code=code, detail=response["message"])
    return response