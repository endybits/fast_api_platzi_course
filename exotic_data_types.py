from enum import Enum

#Pydantic Special Data Types
from pydantic import HttpUrl
from pydantic import FilePath
from pydantic import DirectoryPath
from pydantic import EmailStr
from pydantic import PaymentCardNumber
from pydantic import IPvAnyAddress
from pydantic import NegativeFloat
from pydantic import PositiveFloat
from pydantic import NegativeInt
from pydantic import PositiveInt

from pydantic import BaseModel

class ExoticModel(BaseModel):
    http: HttpUrl
    file: FilePath
    directory: DirectoryPath
    email: EmailStr
    card_number: PaymentCardNumber
    ip: IPvAnyAddress
