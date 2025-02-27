from app.schemas.Movie import MovieResponseSchema
from app.models import movie

from typing import Optional, List

from fastapi import Form


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
            "created_at": mov.created_at,  # Оставляем как datetime
            "updated_at": mov.updated_at,  # Оставляем как datetime
        }
        movies_data.append(MovieResponseSchema(**movie_dict).model_dump())
        processed_ids.add(mov.id)

    return movies_data


async def parse_form_data(
        title: str = Form(...),
        eng_title: Optional[str] = Form(None),
        url: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        avatar: Optional[str] = Form(None),
        release_year: Optional[str] = Form(None),  # если дата, то дополнительное преобразование
        director: Optional[str] = Form(None),
        country: Optional[str] = Form(None),
        part: Optional[int] = Form(None),
        age_restriction: Optional[int] = Form(None),
        duration: Optional[int] = Form(None),
        category_id: Optional[int] = Form(None),
        producer: Optional[str] = Form(None),
        screenwriter: Optional[str] = Form(None),
        operator: Optional[str] = Form(None),
        composer: Optional[str] = Form(None),
        actors: Optional[str] = Form(None),
        editor: Optional[str] = Form(None),
        genres: Optional[List[int]] = Form(None),
):
    def to_list(value: Optional[str]) -> Optional[List[str]]:
        if value:
            return [item.strip() for item in value.split(',') if item.strip()]
        return None

    return {
        "title": title,
        "eng_title": eng_title,
        "url": url,
        "description": description,
        "avatar": avatar,
        "release_year": release_year,
        "director": director,
        "country": country,
        "part": part,
        "age_restriction": age_restriction,
        "duration": duration,
        "category_id": category_id,
        "producer": to_list(producer),
        "screenwriter": to_list(screenwriter),
        "operator": to_list(operator),
        "composer": to_list(composer),
        "actors": to_list(actors),
        "editor": to_list(editor),
        "genres": genres,
    }
