import json
from typing import List
from uuid import uuid4
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models import User, Role

app = FastAPI()

db: List[User] = [
    User(id=uuid4(), 
         first_name="John", 
         last_name="Doe", 
         middle_name="Middle", 
         roles=[ Role.user]),

]

@app.get("/")
async def root():
    with open('departure_info.json', 'r') as json_file:
        data = json.load(json_file)

    return JSONResponse(content=data)

@app.get("/api/v1/users")
async def get_users():
    return db