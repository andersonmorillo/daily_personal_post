from typing import Optional
from pydantic import BaseModel

# Create an ItemBase and UserBase Pydantic models (or let's say "schemas")
# to have common attributes while creating or reading data.


class PetBase(BaseModel):
    name: str
    race: Optional[str]


# And create an ItemCreate and UserCreate that inherit from them
# (so they will have the same attributes), plus any additional data (attributes) needed for creation.
class PetCreate(PetBase):
    pass

# contiene la estructura de las relaciones de la mascota id y owner_id


class Pet(PetBase):
    id: int
    owner_id: int
    # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict,
    # but an ORM model (or any other arbitrary object with attributes).

    class Config:
        orm_mode = True


# base model para el usuario
class UserBase(BaseModel):
    email: str
    username: str
    


class CreateUser(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool = True
    pets: list[Pet] = []

    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str