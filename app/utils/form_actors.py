from app.schemas.Actor import ActorResponseSchema
from app.models.actor import Actor

from typing import Optional


def form_actors_data(actors: list | Optional[Actor]) -> list[dict]:
    actors_data = []
    processed_ids = set()

    for obj in actors:
        if obj.id in processed_ids:
            continue
        else:
            actor_dict = {
                "id": obj.id,
                "first_name": obj.first_name,
                "last_name": obj.last_name,
                "eng_full_name": obj.eng_full_name,
                "biography": obj.biography,
                "avatar": obj.avatar,
                "height": obj.height,
                "date_of_birth": obj.date_of_birth if obj.date_of_birth else None,  # Добавляем поле
                "place_of_birth": obj.place_of_birth if obj.place_of_birth else None,  # Добавляем поле
                "created_at": obj.created_at,      # Оставляем как datetime
                "updated_at": obj.updated_at,      # Оставляем как datetime
            }
            actors_data.append(ActorResponseSchema(**actor_dict).model_dump())
            processed_ids.add(obj.id)

    return actors_data
