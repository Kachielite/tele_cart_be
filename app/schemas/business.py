from typing import Optional


from pydantic import BaseModel


class BusinessRequestSchema(BaseModel):
    name: Optional[str]
    address: Optional[str]
    description: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Business Name",
                "address": "Business Address",
                "description": "Business Description",
            }
        }



class BusinessResponseSchema(BaseModel):
    id: int
    identifier: str
    name: str
    address: Optional[str]
    phone_number: str
    description: Optional[str]
    image_url: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "identifier": "BUS123",
                "name": "Business Name",
                "address": "Business Address",
                "phone_number": "234xxxxxxxxxx",
                "description": "Business Description",
                "image_url": "https://business_image_url.com",
                "created_at": "2021-09-14T13:00:00",
                "updated_at": "2021-09-14T13:00:00"
            }
        }