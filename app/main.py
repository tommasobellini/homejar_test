from typing import List

import bson
from bson import Binary
from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.params import Body
from pymongo import MongoClient
from starlette import status
from starlette.responses import JSONResponse

from business.users.models import UserModel
import uvicorn

config = dotenv_values(".env")

app = FastAPI(
    title="HomeJar - API Service",
    description="API specifications for HomeJar project",
    version="0.0.1",
    docs_url="/homejar/ui/",
    openapi_url="/homejar/openapi.json"
)

@app.on_event("startup")
def startup_db_client():
    uri = "mongodb+srv://root:LnAuiTvj3j98fOPr@cluster0.qkvxyg5.mongodb.net/?retryWrites=true&w=majority"
    # Create a new client and connect to the server
    client = MongoClient(uri)
    app.mongo_client = client
    app.db = client.get_database('home_jar')
    app.users_collection = app.db.get_collection("users")
    try:
        app.mongo_client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongo_client.close()

@app.get("/")
def hello_world():
    return {"message": "This is Home Jar API"}

@app.get("/users", response_description="List all users", response_model=List[UserModel])
async def list_users(limit: int = 15):
    users = list(app.users_collection.find({}).limit(limit))  # Fetch all users from the collection
    return users

@app.post("/users", response_description="Add new user", response_model=UserModel)
async def create_user(body: UserModel = Body(...)):
    existing_user = app.users_collection.find_one({"email": body.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    user_dict = body.model_dump()
    user_dict["id"] = str(user_dict["id"])
    result = app.users_collection.insert_one(user_dict)
    user = app.users_collection.find_one({"_id": result.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=user)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)