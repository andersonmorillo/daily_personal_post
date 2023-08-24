from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from models.models import Pet
from models.models import User as UserModel
from models.models import Pet as PetModel
from schemas.schemas import *
from CRUD import crud
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.database import engine, SessionLocal, Base
from middlewares.jwt_manager import check_password
app = FastAPI()

oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# create all tables in database
Base.metadata.create_all(bind=engine)

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: SessionLocal = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    password_response = check_password(user.hashed_password, form_data.password)
    if not password_response:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"access_token": user.username, "token_type": "bearer"}

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


