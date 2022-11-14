# Python Resources
from typing import Optional

# Pydantic Resources
from pydantic import BaseModel

# FastAPI Resources
from fastapi import FastAPI
from fastapi import Body, Query, Path

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


# Request Body and Response Body
@app.post('/person/new')
async def new_person(person: Person = Body(...)):
    return person


# Validations: Query Parameters
@app.get('/person/detail')
async def detail_person(
    name: Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=20,
        title='Person Name',
        description='This field correspond to the person name'
    ),
    age: Optional[int] = Query(
        default=18,
        ge=18,
        le=99,
        title='Person Age',
        description='This field correspond to the person age'
    )
):
    return {
        "Person": {
            "name": name,
            "age": age
        }
    }


# Validations Path Parameters
@app.get('/person/detail/{person_id}')
async def detail_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This field is the Person ID. It's required and must be greater than zero"
    )
):
    return {
        "Person": {
            "id": person_id,
            "message": "The person ID exists"
        }
    }
