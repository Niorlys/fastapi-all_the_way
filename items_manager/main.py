from fastapi import FastAPI
from routes.items_routes import items
import uvicorn

items_app = FastAPI()
items_app.include_router(items)

@items_app.get('/')
async def index():
    return {"message":"Reinen Tisch Machen"}


if __name__ == '__main__':
    uvicorn.run("main:items_app",host="0.0.0.0",port=8080, reload=True) #Wtih host='0.0.0.0' we are allowing to bind to all availables
                                                                        #networks interfaces, wich is not recommended in production