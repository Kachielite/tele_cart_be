from typing import Optional

from pydantic import BaseModel


class ProductCreationRequest(BaseModel):
    name: str
    description: str
    price: float
    in_stock: bool
    category_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Product 1",
                "description": "Product 1 description",
                "price": 1000.0,
                "in_stock": True,
                "category_id": 1
            }
        }

class ProductUpdateRequest(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    in_stock: Optional[bool]
    category_id: Optional[int]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Product 1",
                "description": "Product 1 description",
                "price": 1000.0,
                "in_stock": True,
                "category_id": 1
            }
        }

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    in_stock: bool
    image_url: str
    category_id: int
    created_at: str
    updated_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Product 1",
                "description": "Product 1 description",
                "price": 1000.0,
                "in_stock": True,
                "image_url": "http://image.com",
                "created_at": "2021-07-01T00:00:00Z",
                "updated_at": "2021-07-01T00:00:00Z"
            }
        }