from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
app.version ="0.0.1"
app.title = "Peliculas"

class Movie(BaseModel):# crear un esquema para generalizar las clases detre las direferentes metodos
    id: Optional[int] = None #requerir un valor como opcional
    title: str = Field(min_length=4, max_length=10, default="mi pelicula")#field sirve para poner reglas y crear valores por defualt 
    overview: str
    year: int
    rating: float
    category: str
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "título",
                "overview": "Descripción de la pelicula",
                "year": 2012,
                "rating": 10,
                "category": "Categoria"
                }
        }

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } ,    {
        'id': 2,
        'title': 'pepe',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } ,    {
        'id': 3,
        'title': 'pablo',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } 
]

@app.get("/", tags=["home"])
def root():
    return "hola"


@app.get("/movies", tags=["movie"])
def get_movies():
    return movies


@app.get("/movies/", tags=["movie"] )
def get_movie_by_query(category: str):
    query = lambda item: item["category"] == category
    return [item for item in movies if item["category"] == category]


@app.get("/movies/{id}", tags=["movie"])
def get_movie(id:int):
    for item in movies:
        if  (item["id"]==id):
            return item
    return []

@app.get('/contact', response_class=HTMLResponse)
def get_list():
    return """
        <h1>Hola soy una pagina</h1>
        <p>soy un parrafo</p>
    """

@app.post("/movies", tags=["movies"])#El metodo body ayuda a evitar que se requieran cada uno de los parametros dentro de la url
def post_movies(id:int = Body(), title:str = Body(), overview:str= Body(),year:int= Body(), rating:float= Body(), category:str= Body()):
    movies.append(
        {
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
        }
    )
    return movies

@app.put("/movies/{id}", tags=["movies"])
def put_movies(id:int, movie :Movie):
    for item in movies:
        if item["id"] == id:
            item["title"]=movie.title
            item["overview"]=movie.overview
            item["year"]=movie.year
            item["rating"]=movie.rating
            item["category"]=movie.category
    return movies

@app.delete("/movies/{id}", tags=["movies"])
def delete_movies(id:int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
    return movies
    