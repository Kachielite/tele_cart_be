from typing import List, Optional

from pydantic import BaseModel

class ProductList(BaseModel):
    id: int
    name: str
    quantity: int
    price: float

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Product 1",
                "quantity": 1,
                "price": 100.0
            }
        }

class OrderResponse(BaseModel):
    id: int
    customer: str
    products: List[ProductList]
    total: float
    status: str
    created_at: str
    updated_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "customer": "Customer 1",
                "products": [
                    {
                        "id": 1,
                        "name": "Product 1",
                        "quantity": 1,
                        "price": 100.0
                    }
                ],
                "total": 100.0,
                "status": "PENDING",
                "created_at": "2021-09-01T00:00:00",
                "updated_at": "2021-09-01T00:00:00"
            }
        }

class OrderRequest(BaseModel):
    customer_name: str
    customer_phone_number: str
    customer_address: str
    customer_telegram_id: int
    products: List[ProductList]

    class Config:
        json_schema_extra = {
            "example": {
                "customer_name": "Customer 1",
                "customer_phone_number": "123",
                "customer_address": "Address 1",
                "customer_telegram_id": 123,
                "products": [
                    {
                        "id": 1,
                        "name": "Product 1",
                        "quantity": 1,
                        "price": 100.0
                    }
                ]
            }
        }