from typing import List, Optional
from pydantic import BaseModel

##MOVIES
class Movie(BaseModel):
    id: int
    name: str
    director: str
    genres: List[str]
    shop: int
    rent: bool = False
    
class MovieRequestCreate(BaseModel):
    name: str
    director: str
    genres: List[str]
    shop: int

class MovieRequestUpdate(BaseModel):
    name: str
    director: str
    genres: List[str]

class MovieRentRequestUpdate(BaseModel):
    rent: bool

##SHOPS!!
class Shop(BaseModel):
    id: int
    address: str
    manager: str
    movies: List[Movie] = []
    
class ShopRequestCreate(BaseModel):
    address: str
    manager: str

class ShopRequestUpdate(BaseModel):
    address: str
    manager: str

class MovieShopRequestUpdate(BaseModel):
    shop: int