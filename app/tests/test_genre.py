from httpx import AsyncClient
from sqlalchemy import insert, select

from app.models.movie import Genre
from conftest import async_session_maker


async def test_add_genre(ac: AsyncClient):
    response = await ac.post("/api/genres/add_genre", data={
        "name": "Тестовый жанр"
    })
    assert response.status_code == 201, f"Ожидался 201, но получен {response.status_code}"
    assert response.json()["message"] == "Жанр успешно добавлен", "Сообщение должно быть 'Жанр успешно добавлен'"


async def test_add_existing_genre(ac: AsyncClient):
    # Сначала добавим жанр
    await ac.post("/api/genres/add_genre", data={"name": "Тестовый жанр"})
    
    # Теперь попробуем добавить его снова
    response = await ac.post("/api/genres/add_genre", data={
        "name": "Тестовый жанр"
    })
    assert response.status_code == 400, f"Ожидался 400, но получен {response.status_code}"
    assert response.json()["error"] == "Такой жанр уже существует.", "Сообщение об ошибке должно быть 'Такой жанр уже существует.'" 
