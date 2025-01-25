from app.schemas.Movie import MovieResponseSchema
from app.models import movie

from typing import Optional


def form_movies_data(movies: list | Optional[movie.Movie]) -> list[dict]:
    movies_data = []
    processed_ids = set()

    for mov in movies:
        if mov.id in processed_ids:
            continue
        movie_dict = {
            "id": mov.id,
            "title": mov.title,
            "eng_title": mov.eng_title,
            "url": mov.url,
            "description": mov.description,
            "avatar": mov.avatar,
            "release_year": mov.release_year,
            "director": mov.director,
            "country": mov.country,
            "part": mov.part,
            "age_restriction": mov.age_restriction,
            "duration": mov.duration,
            "category_id": mov.category_id,
            "producer": mov.producer,
            "screenwriter": mov.screenwriter,
            "operator": mov.operator,
            "composer": mov.composer,
            "actors": mov.actors,
            "editor": mov.editor,
            "genres": [gm.genre_id for gm in mov.genres_link],
            "created_at": mov.created_at,      # Оставляем как datetime
            "updated_at": mov.updated_at,      # Оставляем как datetime
        }
        movies_data.append(MovieResponseSchema(**movie_dict).model_dump())
        processed_ids.add(mov.id)

    return movies_data
