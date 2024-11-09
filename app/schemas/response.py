from pydantic import BaseModel


class GeneralResponseSchema(BaseModel):
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation successful"
            }
        }