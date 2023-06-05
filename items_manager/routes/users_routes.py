from fastapi import APIRouter

users = APIRouter()

@users.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id:int, item_id:int):
    pass