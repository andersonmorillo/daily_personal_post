from fastapi import Body, FastAPI, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Any, Coroutine, Union, Annotated, Optional, List
from actions.funciones import transform_filter
from starlette.requests import Request
from jwt_manager import decode_token, encode_token

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
# Configure CORS settings
origins = [
    "http://localhost:3000",  # Replace with the URL of your Next.js app
]

proyectos = [
    {
        "id": 1,
        "name": "Proyecto 1",
        "descripcion": "El mejor protecto del mundo",
        "tecnologies": ["python"],
        "image": "El Bicho",
        "urlGithub": "link github",
        "urlYoutube": "link",
        "blogContent": "contenido autogenerado"
    },
    {
        "id": 2,
        "name": "Proyecto 2",
        "descripcion": "descripcion",
        "tecnologies": ["python", "nextjs", "react"],
        "image": "no",
        "urlGithub": "link github",
        "urlYoutube": "link youtbe",
        "blogContent": "contenido autogenerado"
    },

]



class User(BaseModel):
    username: str
    password: str


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = decode_token(auth.credentials)
        if data["username"] != "pepe":
            raise HTTPException(
                status_code=403, detail="Credenciales incorrectas")


class Proyecto(BaseModel):
    id: Optional[int] = None
    name: str
    descripcion: str
    tecnologies: List[str]
    image: str
    urlGithub: Optional[str] = None
    urlYoutube: Optional[str] = None
    blogContent: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Proyecto 1",
                "descripcion": "El mejor protecto del mundo",
                "tecnologies": ["python"],
                "image": "El Bicho",
                "urlGithub": "link github",
                "urlYoutube": "link",
                "blogContent": "contenido autogenerado"
            }
        }


# send a proyect
@app.get("/Proyecto/{id}", response_model=Proyecto, tags=["proyecto"])
def get_proyecto(id: int):
    for proyecto in proyectos:
        if proyecto["id"] == id:
            return JSONResponse(content=proyecto)
    return HTTPException(status_code=404, detail="problemas")

# filter a proyects tecnology
@app.get("/proyectos/", tags=["proyecto"], response_model=List[Proyecto])
async def get_proyectos_by_tecnologies(q: str = Query(min_length=3, max_length=15)):
    tecnologia = transform_filter(q,"")
    projectList = []
    for proyecto in proyectos:
        for tecnologie in proyecto["tecnologies"]:
            if tecnologie == tecnologia:
                projectList.append(proyecto)
    return JSONResponse(content=projectList, status_code=200)


@app.get("/proyectos", response_model=List[Proyecto], tags=["proyecto"], status_code=200)
def get_proyectos() -> List[Proyecto]:
    return JSONResponse(content=proyectos, status_code=200)


#create project
@app.post("/proyecto", tags=["proyecto"], response_model=dict)
def create_project(project: Proyecto) -> dict:
    proyectos.append(project)
    return JSONResponse(content={"message":"proyecto creado"}, status_code=201)
 
#update a project
@app.put("/proyecto/{id}", tags=["proyecto"], response_model=dict)
def update_project(id: int, project: Proyecto) -> dict:
    for proyecto in proyectos:
        if proyecto["id"]  == id:
            proyecto['name'] = project.name      
            proyecto['descripcion'] = project.descripcion       
            proyecto['tecnologies'] = project.tecnologies        
            proyecto['urlGithub'] = project.urlGithub     
            proyecto['urlYoutube'] = project.urlYoutube 
            proyecto['image'] = project.image
            proyecto['blogContent'] = project.blogContent
            return JSONResponse( content={"message": f"Se ha modificado el proyecto {id}"}, status_code=200)
    raise HTTPException(status_code=404, detail="no project ID")

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
