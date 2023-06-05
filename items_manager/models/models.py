from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Item(BaseModel):
    id:Optional[int]
    name:str
    description:str
    created_at:Optional[datetime]
    updated_at:Optional[datetime]

    class Config:
        schema_extra = {
        "example": {
        "name": "Candy box",
        "description": "Something to respond with in Halloween"
        }
        }

class ItemPUT(BaseModel):
    name:Optional[str]
    description:Optional[str]