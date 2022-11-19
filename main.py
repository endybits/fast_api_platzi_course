# Python Resources
from typing import Optional
from enum import Enum

# Pydantic Resources
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# FastAPI Resources
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Cookie, Header, UploadFile, File

app = FastAPI()

# Other Classes
class HairColor(Enum):
    black= 'black'
    white= 'white'
    brown= 'brown'
    red= 'red'
    blonde= 'blonde'


# Models

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Endy'
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Bermudez'
    )
    age: int = Field(
        ...,
        ge=18,
        lt=100,
        example=37
    )
    email: EmailStr
    hair_color: Optional[HairColor] = Field(default=None, example='red')
    is_married: Optional[bool] = Field(default=None, example=True)
class Person(PersonBase):
    password: str = Field(
        ...,
        min_length=8,
        example='P@ssw0rd'
    )

    """
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
    """
class PersonOut(PersonBase):
    pass

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=2,
        max_length=40,
        example='RCH'
    )
    state: str = Field(
        ...,
        min_length=2,
        max_length=40,
        example='GJR'
    )
    country: str = Field(
        ...,
        min_length=2,
        max_length=40,
        example= 'CO'
    )
    """
    class Config:
        schema_extra = {
            'example': {
                'city': 'Riohacha',
                'state': 'La Guajira',
                'country': 'CO'
            }
        }
    """

class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example='@endyb')
    message: str = Field(default="Login Successfully")


@app.get(
    path='/',
    status_code=status.HTTP_200_OK,
    tags=['Home'],
    summary='First example'
)
async def home():
    """
        Home

        This path operation shows a basic axample to test if the server is Ok!

        Parameters:
        - None

        Returns a simple hello world dict
    """

    return {"greeting": {"Hello": "World FastAPI."}}


# Request Body and Response Body
@app.post(
    path='/person/new',
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=['Person'],
    summary='Create Person in the app'
)
async def create_person(person: Person = Body(...)):
    """
        Create Person

        This path operation creates a person in the app and save the information in Database

        Parameters:
        - Request body parameter
            - **person: Person** -> A person model with first name, last name, age, hair color and marital status
        
        Returns a person model with first name, lasta name, age, hair color and marital status
    """
    return person


# Validations: Query Parameters
@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK,
    tags=['Person'],
    deprecated=True
)
async def detail_person(
    name: Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=20,
        title='Person Name',
        description='This field correspond to the person name',
        example='Lina'
    ),
    age: Optional[int] = Query(
        default=18,
        ge=18,
        le=99,
        title='Person Age',
        description='This field correspond to the person age',
        example=26
    )
):
    return {
        "Person": {
            "name": name,
            "age": age
        }
    }


# Validations Path Parameters
persons = [1, 2, 3, 4, 5]

@app.get(
    path='/person/detail/{person_id}',
    status_code=status.HTTP_200_OK,
    tags=['Person']
)
async def detail_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This field is the Person ID. It's required and must be greater than zero",
        example=22222
    )
):
    """
        Get Detail Person

        This path operation get a specific person in the Database of this app.

        Parameters:
        - Path parameter
            - **person_id: int**
        
        Returns a person model with first name, lasta name, age, hair color and marital status
    """

    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= {
                'Error': True,
                'message': 'This person doesn\'t exists!'
            }
        )
    return {
        "Person": {
            "id": person_id,
            "message": "The person ID exists"
        }
    }


# Validation Request Body
@app.put(
    path='/person/{person_id}',
    status_code=status.HTTP_200_OK,
    tags=['Person']
)
async def update_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This field is the Person ID. It's required and must be greater than zero",
        example=1111
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    """
        Update a Person

        This path operation updates a specific person in the Database of this app.

        Parameters:
        - Path parameter
            - **person_id: int**
        - Request body parameter
            - **person: Person** -> A person model with first name, last name, age, hair color and marital status
            - **location: Location** -> A location model with city, state, and country fields
        
        Returns a mixed dict between person model and location model.  Fields: first name, last name, age, hair color, marital status, city, state, and country.
    """

    results = person.dict()
    results.update(location.dict())
    #results = person.dict() | location.dict()
    return results

# Forms
@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=['Person']
)
async def login(
    username: str = Form(...),
    password: str = Form(...)
):
    """
        Login

        This path operation allows a person to login in the app.

        Parameters:
        - Form parameters
            - **username: str**
            - **password: str**
        
        Returns a person model with first name, last name, age, hair color and, marital status.
    """

    return LoginOut(username=username)


# Cookies and Header parameters
@app.post(
    path='/contac-us',
    status_code=status.HTTP_200_OK,
    tags=['Contact-us']
)
async def contact_us(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
        example='Endy'
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
        example='Bermudez'
    ),
    email: EmailStr = Form(
        ...,
        example='endyb@mail.on'
    ),
    message: str = Form(
        ...,
        min_length=20,
        example='This is a test message!'
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    """
        Contact us

        This path operation allows an user to contact the app personal to exclusive treatment about somewhere topic.

        Parameters:
        - Form parameters
            - **first_name: str**
            - **last_name: str**
            - **email: EmailStr**
            - **message: str**
        - Header parameters
            - **user_agent: Optional[str]**
        - Cookies parameters
            - **ads: Optional[str]**
        
        Returns the user agent data, catched from the user 
    """

    return user_agent


# Files
@app.post(
    path='/post-image',
    status_code=status.HTTP_200_OK,
    tags=['Files']
)
async def upload_image(
    image: UploadFile = File(...)
):
    """
        Upload an Image

        This path operation allows an user to Upload a Image File.

        Parameters:
        - File parameters
            - **image: UploadFile**
        
        Returns the filename, format and size from the uploaded image. 
    """

    return {
        'Filename': image.filename,
        'Format': image.content_type,
        'Size(Kb)': round(len(image.file.read())/1024, 2)
    }