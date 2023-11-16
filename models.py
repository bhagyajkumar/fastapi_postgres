from datetime import datetime, timedelta

from fastapi import HTTPException
from db import db
from pydantic import BaseModel
from uuid import uuid4
import bcrypt
import jwt
import os


class Item(BaseModel):
    name:str
    price: float

    
    def create(self):
        cursor = db.cursor()
        cursor.execute("INSERT INTO item (id, name, price) VALUES (%s,%s,%s)", [uuid4(),self.name, self.price])
        db.commit()
        cursor.close()

class ItemGet(Item):
    id: str

    @classmethod
    def get_all(cls):
        cursor = db.cursor()
        cursor.execute("SELECT id, name, price FROM item;")
        result = cursor.fetchall()
        items = []
        for i in result:
             items.append(cls(id=str(i[0]), name=i[1], price=i[2]))
            
        return items


class SignupInputModel(BaseModel):
    email:str
    username:str
    password:str

    def save(self):
        password_bytes = self.password.encode()
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(password_bytes, salt)
        password_hash = hash.decode()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO users (id, username, email, password_hash) values (%s, %s, %s, %s)',
            [uuid4(), self.username, self.email, password_hash]
        )
        db.commit()

class LoginOutputModel(BaseModel):
    access_token:str
    refresh_token:str

class LoginInputModel(BaseModel):
    username:str
    password:str

    def check_password(self, password, password_hash):
        if bcrypt.checkpw(self.password.encode(), password_hash.encode()):
            return True
        
    def get_jwt_tokens(self):
        cursor = db.cursor()
        cursor.execute("SELECT id, password_hash from users where username = %s", [self.username]); 
        user_id, password_hash = cursor.fetchone()

        if(self.check_password(self.password,password_hash)):
            access_token_payload = {
                "user_id": str(user_id) or None,
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(minutes=15)  # Adjust the expiration time as needed
            }
            access_token = jwt.encode(
                access_token_payload,
                os.environ.get("ACCESS_SECRET", "access_secret"),
                algorithm="HS256"
            )

            refresh_token_payload = {
                "user_id": str(user_id) or None,
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(days=7)  # Adjust the expiration time as needed
            }
            refresh_token = jwt.encode(
                refresh_token_payload,
                os.environ.get("REFRESH_SECRET", "refresh_secret"),
                algorithm="HS256"
            )

            
            return LoginOutputModel(access_token=access_token, refresh_token=refresh_token)
        else:
            raise HTTPException(status_code=401)



