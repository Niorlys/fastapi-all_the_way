import pytest
from httpx import AsyncClient
from main import items_app
from datetime import datetime, timedelta


@pytest.fixture
def client():
    return AsyncClient(app=items_app, base_url="http://testserver")

@pytest.mark.asyncio
async def test_create_item(client):
    item = {"id": 1, "name": "Ice cream bucket", "description": "Delight"}
    response = await client.post("/item", json=item)
    assert response.status_code == 200
    assert response.json() =={"message":f"Item 1 created successfully"}


@pytest.mark.asyncio
async def test_get_items(client):
    REFERENC_DT_CREATED = REFERENC_DT_UPDATED = datetime.now()
    response = await client.get("/item/1")
    status_code = response.status_code
    response = response.json()
    created_at, updated_at = response.pop('created_at'), response.pop('updated_at')
    assert status_code == 200
    assert REFERENC_DT_CREATED - datetime.strptime(created_at,'%d-%m-%Y %H:%M:%S') < timedelta(seconds=3)\
                            and REFERENC_DT_UPDATED - datetime.strptime(updated_at,'%d-%m-%Y %H:%M:%S')< timedelta(seconds=3) 
    assert response == {"id": 1, "name": "Ice cream bucket", "description": "Delight"}


@pytest.mark.asyncio
async def test_update_item(client):
    item = {"name": "Cookies", "description": "mmmm"}
    updated_item =  {"name": "Cookies 2", "description": "mmmm 2"}
    await client.post("/item", json=item)
    REFERENC_DT_CREATED = REFERENC_DT_UPDATED = datetime.now()
    response = await client.put("/item/1", json=updated_item)
    status_code = response.status_code
    response = response.json()
    created_at, updated_at = response.pop('created_at'), response.pop('updated_at')
    assert status_code == 200
    assert response.pop('id') == 1
    assert REFERENC_DT_CREATED - datetime.strptime(created_at,'%d-%m-%Y %H:%M:%S') < timedelta(seconds=3)\
                            and REFERENC_DT_UPDATED - datetime.strptime(updated_at,'%d-%m-%Y %H:%M:%S')< timedelta(seconds=3) 
    assert response == updated_item
    

@pytest.mark.asyncio
async def test_delete_item(client):
    item = {"name": "Caviar", "description": "Salmon"}
    await client.post("/item", json=item)
    response = await client.delete("/item/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Item 1 deleted successfully"}