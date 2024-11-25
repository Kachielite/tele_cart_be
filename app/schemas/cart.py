from pydantic import BaseModel


class CartResponse(BaseModel):
    id: int
    business_id: int
    customer_id: int
    product_id: int
    added_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "business_id": 12,
                "customer_id": 23,
                "product_id": 2,
                "added_at": "2021-07-01T00:00:00Z"
            }
        }
