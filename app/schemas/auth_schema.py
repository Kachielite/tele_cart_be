from pydantic import BaseModel


class AuthResponseSchema(BaseModel):
    access_token: str
    token_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "xxxxxxxx",
                "token_type": "bearer"
            }
        }


class AuthRequestSchema(BaseModel):
    business_name: str
    phone_number: str
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "business_name": "Business Name",
                "phone_number": "234xxxxxxxxxx",
                "email": "business@mail.com",
                "password": "password"
            }
        }

class CurrentBusinessResponse(BaseModel):
    id: int
    business_name: str
    identifier: str

    class Config:
        json_schema_extra = {
            "example":{
                "id": 223,
                "business_name": "Business Name",
                "identifier": "BUS3674"
            }
        }
