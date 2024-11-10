from pydantic import BaseModel


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Category",
                "description": "Category description"
            }
        }