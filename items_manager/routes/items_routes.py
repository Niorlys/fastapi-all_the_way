from fastapi import APIRouter
from database.connection import Connection
from models.models import Item, datetime, ItemPUT
from typing import Union

items = APIRouter()
conn = Connection()

@items.post('/item')
async def create_item(data:Item):
    data.created_at = data.updated_at = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    instance = conn.create_record(data)
    return {"message":f"Items {instance.id} created successfully at {data.created_at}"}

@items.get('/item/{id}')
async def get_item(id:int):
    data = conn.get_record(Item, id)
    return data

@items.get('/item/filter/')
async def get_items_filtered(lasts:int, desc:bool = True, optional = None):#Pending filtering with optional parameters set with type Union[...,None]
    return conn.get_filtered(Item, lasts, desc)

@items.put('/item/{id}')
async def update_item(id:int, body:ItemPUT):
    body = vars(body)
    data = {key:body[key] for key in body if body[key]}
    data['updated_at'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    return conn.update_record(Item,id, **data)

@items.delete('/item/{id}')
async def delete_item(id:int):
    result = conn.delete_record(Item,id)
    if result:
        return {"message":f"Item {id} deleted succesfully"}
    return {"message":f"Item {id} could not be deleted, it seems tha it was deleted alredy."}


