# Python Resources
from typing import Optional
from enum import Enum

# Pydantic Resources
from pydantic import BaseModel
from pydantic import Field, EmailStr

# FastAPI Resources
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Other Classes
class HairColor(Enum):
    black= 'black'
    white= 'white'
    brown= 'brown'
    red= 'red'
    blonde= 'blonde'


# Models
class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        ge=18,
        le=99
    )
    email: EmailStr
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=False)

    class Config:
        schema_extra = {
            'example': {
                'first_name': 'Endy',
                'last_name': 'Bermudez',
                'age': 36,
                'email': 'endyb.dev@gmail.com',
                'hair_color': 'black',
                'is_married': True
            }
        }

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=2,
        max_length=40
    )
    state: str = Field(
        ...,
        min_length=2,
        max_length=40
    )
    country: str = Field(
        ...,
        min_length=2,
        max_length=40
    )
    class Config:
        schema_extra = {
            'example': {
                'city': 'Riohacha',
                'state': 'La Guajira',
                'country': 'CO'
            }
        }


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


# Validation Request Body
@app.put('/person/{person_id}')
async def upload_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This field is the Person ID. It's required and must be greater than zero"
    ),
    person: Person = Body(...),
    #location: Location = Body(...)
):
    #results = person.dict()
    #results.update(location.dict())
    #results = person.dict() | location.dict()
    #return results
    return person