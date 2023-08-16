from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Union, Annotated, Optional, List

app = FastAPI()

# Configure CORS settings
origins = [
    "http://localhost:3000",  # Replace with the URL of your Next.js app
]

dataBase = [
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

class Proyectos(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: str
    imagen: str
    urlGithub: Optional[str] = None
    urlYoutube: Optional[str] = None
    blogContent: Optional[str] = None

    class Config:
        pass
    schema_extra = {
        "example": {
            "id": 1,
            "nombre": "Proyecto 1",
            "descripcion": "El mejor protecto del mundo",
            "imagen": "El Bicho",
            "urlGithub": "link github",
            "urlYoutube": "link",
            "blogContent": "contenido autogenerado"
        }
    }

#Send the proyects:
@app.get("/", response_model=List[Proyectos], tags=["proyecto"])
def get_proyects() -> List[Proyectos]:
    return JSONResponse(content=dataBase, status_code=200)



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


