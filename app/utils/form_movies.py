from app.schemas.Movie import MovieResponseSchema

import json
from typing import List, Union

def parse_string_to_list(value: Union[str, List[str], None]) -> List[str]:
    """Преобразует строку в список. Если значение уже список, возвращает его."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    try:
        # Удаляем лишние символы и преобразуем строку в список
        value = value.strip()
        if value.startswith("{") and value.endswith("}"):
            value = "[" + value[1:-1] + "]"
        return json.loads(value)
    except (json.JSONDecodeError, AttributeError):
        return []

def form_movies_data(movies: list) -> list[dict]:
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
            "operator": parse_string_to_list(movie.operator) if hasattr(movie, "operator") else [],
            "composer": parse_string_to_list(movie.composer) if hasattr(movie, "composer") else [],
            "actors": parse_string_to_list(movie.actors) if hasattr(movie, "actors") else [],
            "editor": parse_string_to_list(movie.editor) if hasattr(movie, "editor") else [],
        }
        movies_data.append(MovieResponseSchema(**movie_dict).dict())
    return movies_data