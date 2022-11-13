# Python Resources
from typing import Optional

# Pydantic Resources
from pydantic import BaseModel

# FastAPI Resources
from fastapi import FastAPI
from fastapi import Body

app = FastAPI()

# Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get('/')
async def home():
    return {"greeting": {"Hello": "World FastAPI."}}


# Request and Response Body
@app.post('/person/new')
async def new_person(person: Person = Body(...)):
    return person