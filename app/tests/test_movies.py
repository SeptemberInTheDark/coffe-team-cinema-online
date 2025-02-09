import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select

from app.models.movie import Movie
from conftest import async_session_maker


@pytest.mark.asyncio
async def test_add_movie(ac: AsyncClient):
    await ac.post("/api/genres/add_genre", data={
        "name": "Жанр Один"
    })
    response = await ac.post("/api/movies/add_movie", data={
        "title": "Тестовый фильм",
        "eng_title": "Test film",
        "url": "http://example.com/test-movie",
        "description": "Описание тестового фильма.",
        "avatar": "http://example.com/photo.jpg",
        "release_year": "2025-02-09",
        "director": "Тестовый режиссер",
        "country": "Тестовая страна",
        "part": 1,
        "age_restriction": 18,
        "duration": 120,
        "category_id": 1,
        "producer": ["producer 1","producer 2"],
        "screenwriter": ["screenwriter 1","screenwriter 2"],
        "operator": ["operator 1","operator 2"],
        "composer": ["composer 1","composer 2"],
        "actors": ["actors 1", "actors 2"],
        "editor": ["editor 1", "editor 2"],
        "genres": [1, 2],
    })
    
    print(response.text)  # Выводим текст ответа для отладки
    assert response.status_code == 201, f"Ожидался 201, но получен {response.status_code}"

    
    # Проверяем содержимое ответа
    print(response.text)  # Выводим текст ответа для отладки


@pytest.mark.asyncio
async def test_search_movies_by_title_and_description(ac: AsyncClient):
    response = await ac.get("/api/movies/search_movies_by_title_and_description", params={"query": "Тест"})
    assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code}"


@pytest.mark.asyncio
async def test_search_movies_by_genre(ac: AsyncClient):
    response = await ac.get("/api/movies/search_movies_by_genre", params={"genre": "Боевик"})
    assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code}"
