from models import models
from schemas import schemas
from middlewares import jwt_manager
from sqlalchemy.orm import Session

# I need to create a pet and user CRUD, remember that CRUD means Create, Read, Update, Delete.
# so let create a function for each one of them. firts let's create a pet.


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.CreateUser):
    hashed_password = jwt_manager.hash_password(user.password)
    db_user = models.User(email=user.email, username=user.username,
                          hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def register_pet(db: Session, user_id: int, pet: schemas.PetCreate):
    pets_list = models.Pet(**pet.dict(), owner_id=user_id) 
    db.add(pets_list)
    db.commit()
    db.refresh(pets_list)
    return pets_list


def get_pets(db:Session, skip: int=0, limit: int=100):
    return db.query(models.Pet).offset(skip).limit(limit).all()


def get_pets_by_user(db:Session, current_user: models.User, skip: int=0, limit: int=10):
    pets = current_user.pets
    return pets
