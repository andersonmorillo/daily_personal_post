from models import models
from schemas import schemas
from middlewares import jwt_manager
from sqlalchemy.orm import Session

# I need to create a pet and user CRUD, remember that CRUD means Create, Read, Update, Delete.
# so let create a function for each one of them. firts let's create a pet.


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


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
