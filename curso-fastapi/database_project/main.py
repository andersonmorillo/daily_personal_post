from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from models.models import Pet
from models.models import User as UserModel
from models.models import Pet as PetModel
from schemas.schemas import *
from CRUD import crud
from config.database import engine, SessionLocal, Base

app = FastAPI()

# create all tables in database
Base.metadata.create_all(bind=engine)

# dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/{id}")
def get_user(id: int, db: SessionLocal = Depends(get_db)):
    return crud.get_user(db=db, user_id=id)


@app.post("/users/", response_model=dict)
def create_user(user: CreateUser, db: SessionLocal = Depends(get_db)) -> dict:
    crud.create_user(db, user)
    return JSONResponse(content={"responce": "usuario agregado"}, status_code=201)


# get all users in the database
@app.get("/users/")
def get_all_users(db: SessionLocal = Depends(get_db)):
    return crud.get_users(db=db)
