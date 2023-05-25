from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel # rename to prevent conflict with class Movie
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer

movie_router = APIRouter()

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating:float = Field(ge=1, le=10)
    category:str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 9.8,
                "category" : "Acción"
            }
        }


# @movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200)
@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "no encontrado"})
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    # data = [ item for item in movies if item['category'] == category ]
    if not result:
        return JSONResponse(status_code=404, content={'message': f"no encontrados {category}"})
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session() # create session
    # MovieModel(title=movie.title, category=movie.category)
    new_movie = MovieModel(**movie.dict()) # ** -> means pass as parameters, dict() -> change to dictionary
    db.add(new_movie)
    db.commit()
    # movies.append(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie)-> dict:
    db = Session() # create session
    result = db.query(MovieModel).filter(MovieModel.id == id).first()

    if not result:
        return JSONResponse(status_code=404, content={'message': "no encontrado"})
    result.title = movie.title
    result.category = movie.category
    result.overview = movie.overview
    result.rating = movie.rating
    result.year = movie.year
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha actualizado la película"})

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int)-> dict:
    db = Session() # create session
    result = db.query(MovieModel).filter(MovieModel.id == id).first()

    if not result:
        return JSONResponse(status_code=404, content={'message': "no encontrado"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"})
