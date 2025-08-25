from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Dict, Optional

from src.constants import MOVIE_NOT_FOUND_MESSAGE, SHOP_NOT_FOUND_MESSAGE
from src.schemas.schemas import Movie, MovieRequestCreate, MovieRequestUpdate, MovieShopRequestUpdate, Shop, ShopRequestCreate, ShopRequestUpdate, MovieRentRequestUpdate

# In-memory "DB"
movies: Dict[int, Movie] = {}
shops: Dict[int, Shop] = {}
_next_movie_id = 1
_next_shop_id = 1

router = APIRouter()

# Movies
@router.get("/movies", response_model=List[Movie])
def read_all_movies():
  return list(movies.values())

@router.get("/movies/{movie_id}", response_model=Movie)
def read_movie_by_id(movie_id : int):
  if movie_id not in movies.keys():
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[MOVIE_NOT_FOUND_MESSAGE])
  return movies[movie_id]

@router.post("/movies", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie : MovieRequestCreate):
  global _next_movie_id

  if movie.shop not in shops.keys():
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[SHOP_NOT_FOUND_MESSAGE])
  
  new_movie = Movie(id=_next_movie_id, **movie.model_dump())
  movies[_next_movie_id] = new_movie
  shops[movie.shop].movies.append(new_movie)
  
  _next_movie_id += 1
  return new_movie

@router.put("/movies/{movie_id}", response_model=Movie)
def update_movie(movie_id : int, new_movie : MovieRequestUpdate):
  if movie_id not in movies.keys():
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[MOVIE_NOT_FOUND_MESSAGE])
  movies[movie_id].name = new_movie.name
  movies[movie_id].director = new_movie.director
  movies[movie_id].genres = new_movie.genres
  return movies[movie_id]

@router.patch("/movies/{movie_id}/rent", response_model=Movie)
def update_rent_movie(movie_id: int, rent_update: MovieRentRequestUpdate):
  if movie_id not in movies.keys():
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[MOVIE_NOT_FOUND_MESSAGE])
  movies[movie_id].rent = rent_update.rent
  return movies[movie_id]


@router.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id : int):
  if movie_id not in movies.keys():
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[MOVIE_NOT_FOUND_MESSAGE])
  movie=movies[movie_id]
  old_shop = movie.shop
  shops[old_shop].movies.remove(movie)
  _ = movies.pop(movie_id)


# Shops
@router.get("/shops", response_model=List[Shop])
def read_all_shops():
  return list(shops.values())

@router.get("/shops/{shop_id}", response_model=Shop)
def read_shop_by_id(shop_id : int):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[SHOP_NOT_FOUND_MESSAGE])
  return shops[shop_id]

@router.post("/shops", response_model=Shop, status_code=status.HTTP_201_CREATED)
def create_shop(shop : ShopRequestCreate):
  global _next_shop_id
  new_shop = Shop(id=_next_shop_id, **shop.model_dump())
  shops[_next_shop_id] = new_shop
  _next_shop_id += 1
  return new_shop

@router.put("/shops/{shop_id}", response_model=Shop)
def update_shop(shop_id : int, new_shop : ShopRequestUpdate):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[SHOP_NOT_FOUND_MESSAGE])
  shops[shop_id].address = new_shop.address
  shops[shop_id].manager = new_shop.manager
  return shops[shop_id]

@router.delete("/shops/{shop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shop(shop_id: int):
    if shop_id not in shops.keys():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[SHOP_NOT_FOUND_MESSAGE])
    
    movies_to_delete = [key for key, value in movies.items() if value.shop == shop_id]

    for movie_id in movies_to_delete:
        movies.pop(movie_id)

    _ = shops.pop(shop_id)

# Extra
@router.get("/shops/{shop_id}/movies", response_model=List[Movie])
def get_all_movies_by_shop(shop_id: int):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[SHOP_NOT_FOUND_MESSAGE])
  return shops[shop_id].movies

@router.get("/shops/{shop_id}/movies/available", response_model=List[Movie])
def get_all_availables_movies_by_shop(shop_id: int):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[SHOP_NOT_FOUND_MESSAGE])
  all_movies = shops[shop_id].movies
  available_movies = [movie for movie in all_movies if not movie.rent]
  return available_movies

@router.patch("/movies/{movie_id}/move", response_model=Movie)
def change_movie_shop(movie_id : int, new_movie_shop : MovieShopRequestUpdate):
  if movie_id not in movies.keys():
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[MOVIE_NOT_FOUND_MESSAGE])
  
  if new_movie_shop.shop not in shops.keys():
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[SHOP_NOT_FOUND_MESSAGE])

  movie = movies[movie_id]
  old_shop = movie.shop
  new_shop = new_movie_shop.shop

  shops[old_shop].movies.remove(movie)
  shops[new_shop].movies.append(movie)
  movie.shop = new_shop
  return movie

@router.get("/search/movies", response_model=List[Movie])
def get_movies_by_values(
    name: Optional[str] = None,
    director: Optional[str] = None,
    genres: Optional[List[str]] = Query(None)
):
    results = list(movies.values())

    if name:
        results = [m for m in results if name.lower() in m.name.lower()]

    if director:
        results = [m for m in results if director.lower() in m.director.lower()]

    if genres:
        results = [m for m in results if all(g in m.genres for g in genres if g != "")]

    return results
  