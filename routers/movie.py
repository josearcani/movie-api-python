from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie
# from models.movie import Movie as MovieModel
# rename to prevent conflict with class Movie
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

# @movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200)
@movie_router.get(
        '/movies',
        tags=['movies'],
        response_model=List[Movie],
        status_code=200,
        dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    # result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get(
        '/movies/{id}',
        tags=['movies'],
        response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    # result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "no encontrado"})
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.get(
        '/movies/',
        tags=['movies'],
        response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    # result = db.query(MovieModel).filter(MovieModel.category == category).all()
    # data = [ item for item in movies if item['category'] == category ]
    if not result:
        return JSONResponse(status_code=404, content={'message': f"no encontrados {category}"})
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.post(
        '/movies',
        tags=['movies'],
        response_model=dict,
        status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session() # create session
    # MovieModel(title=movie.title, category=movie.category)
    MovieService(db).create_movie(movie)
    # new_movie = MovieModel(**movie.dict()) # ** -> means pass as parameters, dict() -> change to dictionary
    # db.add(new_movie)
    # db.commit()
    # movies.append(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})

@movie_router.put(
        '/movies/{id}',
        tags=['movies'],
        response_model=dict,
        status_code=200)
def update_movie(id: int, movie: Movie)-> dict:
    db = Session() # create session
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "no encontrado"})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": "Se ha actualizado la película"})

@movie_router.delete(
        '/movies/{id}',
        tags=['movies'],
        response_model=dict,
        status_code=200)
def delete_movie(id: int)-> dict:
    db = Session() # create session
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "no encontrado"})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"})
