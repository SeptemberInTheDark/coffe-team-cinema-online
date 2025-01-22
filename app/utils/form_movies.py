from app.schemas.Movie import MovieResponseSchema
from app.models import movie

from typing import Optional


def form_movies_data(movies: list | Optional[movie.Movie]) -> list[dict]:
    movies_data = []
    for movie in movies:
        movie_dict = {
            "id": movie.id,
            "title": movie.title,
            "eng_title": movie.eng_title,
            "url": movie.url,
            "description": movie.description,
            "avatar": movie.avatar,
            "release_year": movie.release_year.isoformat() if movie.release_year else None,
            "director": movie.director,
            "country": movie.country,
            "part": movie.part,
            "age_restriction": movie.age_restriction,
            "duration": movie.duration,
            "category_id": movie.category_id,
            "producer": movie.producer,
            "screenwriter": movie.screenwriter,
            "operator": movie.operator,
            "composer": movie.composer,
            "actors": movie.actors,
            "editor": movie.editor,
            "genres": movie.genres,
        }
        movies_data.append(MovieResponseSchema(**movie_dict).dict())
    return movies_data