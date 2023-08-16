from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Any, Coroutine, Union, Annotated, Optional, List

from starlette.requests import Request
from jwt_manager import decode_token, encode_token

app = FastAPI()

# Configure CORS settings
origins = [
    "http://localhost:3000",  # Replace with the URL of your Next.js app
]

proyectos = [
    {
        "id": 1,
        "nombre": "Proyecto 1",
        "descripcion": "El mejor protecto del mundo",
        "imagen": "El Bicho",
        "urlGithub": "link github",
        "urlYoutube": "link",
        "blogContent": "contenido autogenerado"
    },
    {
        "id": 2,
        "nombre": "Proyecto 2",
        "descripcion": "descripcion",
        "imagen": "no",
        "urlGithub": "link github",
        "urlYoutube": "link youtbe",
        "blogContent": "contenido autogenerado"
    }
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class User(BaseModel):
    username: str
    password: str

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = decode_token(auth.credentials)
        if data["username"] != "andersonmorillo":
            raise HTTPException(status_code=403, detail="Credenciales incorrectas")

class Proyecto(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: str
    tecnologias: list 
    imagen: str 
    urlGithub: Optional[str] = None
    urlYoutube: Optional[str] = None
    blogContent: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Proyecto 1",
                "descripcion": "El mejor protecto del mundo",
                "tecnologias": ["python"],
                "imagen": "El Bicho",
                "urlGithub": "link github",
                "urlYoutube": "link",
                "blogContent": "contenido autogenerado"
            }
        }

#Send the proyects:
@app.get("/proyecto", response_model=List[Proyecto], tags=["proyecto"])
def get_proyects() -> List[Proyecto]:
    return JSONResponse(content=proyectos, status_code=200)


#send a proyect
@app.get("/Proyecto/{id}", response_model=Proyecto, tags= ["proyecto"])
def get_proyecto(id: int):
    for proyecto in proyectos:
        if proyecto["id"] == id:   
            return JSONResponse(content=proyecto)
    return JSONResponse({"mensaje":"no se encontró el proyecto"})

#filter a proyects
@app.get("/proyectos", response_model=List[Proyecto], tags=["proyecto"])
def get_proyecto():
    return "sola"

@app.get("/markdown", response_class=HTMLResponse)
def render_markdown():
    file_path = "template_example.md"  # Replace with the actual path to your file

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    markdown_content = "# Hello, *FastAPI*!\nThis is **Markdown** content."
    return str(file_content)


