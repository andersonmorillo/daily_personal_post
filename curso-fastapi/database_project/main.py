from middlewares.jwt_manager import *
from config.database import engine, SessionLocal, Base
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from CRUD import crud
from schemas.schemas import *
from models.models import Pet as PetModel
from models.models import User as UserModel
from fastapi.responses import JSONResponse
from fastapi import Depends, FastAPI, HTTPException, status
from typing import Annotated
from jose import JWTError
from passlib.context import CryptContext
SECRET_KEY = "secreto"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# create all tables in database
Base.metadata.create_all(bind=engine)

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(SessionLocal(), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},  expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: Annotated[str, Depends(oath2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_data = decode_token(token)
        username: str = user_data.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(DB, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.is_active:
        print(current_user.is_active)
        raise HTTPException(status_code=400, detail="la cuestion es false")
    return current_user


@app.get("/users/me/", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@app.get("/users/me/pets/")
async def read_own_items(
        current_user: Annotated[User, Depends(get_current_active_user)]):
    return crud.get_pets_by_user(DB, current_user=current_user)


@app.post("/users/me/pets/")
async def register_pet(pet: PetCreate, current_user: Annotated[User, Depends(get_current_active_user)]):
    return crud.register_pet(DB, current_user.id, pet)
    



@app.get("/users/{id}")
def get_user_info(id: int, db: SessionLocal = Depends(get_db)):
    return crud.get_user(db=db, user_id=id)


@app.post("/users/", response_model=dict)
def create_user(user: CreateUser, db: SessionLocal = Depends(get_db)) -> dict:
    crud.create_user(db, user)
    return JSONResponse(content={"responce": "usuario agregado"}, status_code=201)


# get all users in the database
@app.get("/users/")
def get_all_users(db: SessionLocal = Depends(get_db)):
    return crud.get_users(db=db)
