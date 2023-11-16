from fastapi import FastAPI
from typing import List
from db import db
from models import Item, ItemGet, LoginInputModel, LoginOutputModel, SignupInputModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def root():
    print(db)
    return {"hello" : "world"}

@app.post("/item")
def create_item(item:Item):
    item.create()

@app.get("/item", response_model=List[ItemGet])
def get_items():
    data = ItemGet.get_all()
    return data

@app.post("/signup", status_code=201)
def create_user(item:SignupInputModel):
    item.save()
    return {
        "message": "user created"
    }

@app.post("/login", response_model=LoginOutputModel)
def login(item:LoginInputModel):
    tokens = item.get_jwt_tokens()
    return tokens 
