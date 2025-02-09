import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select

from app.models.movie import Genre
from conftest import async_session_maker


@pytest.mark.asyncio
async def test_add_genre(ac: AsyncClient):
    response = await ac.post("/api/v1/api/genres/add_genre", data={
        "name": "Тестовый жанр2"
    })
    assert response.status_code == 201, f"Ожидался 201, но получен {response.status_code}"
    assert response.json()["message"] == "Жанр успешно добавлен", "Сообщение должно быть 'Жанр успешно добавлен'"


@pytest.mark.asyncio
async def test_add_existing_genre(ac: AsyncClient):
    # Сначала добавим жанр
    await ac.post("/api/v1/api/genres/add_genre", data={"name": "Тестовый жанр"})
    
    # Теперь попробуем добавить его снова
    response = await ac.post("/api/v1/api/genres/add_genre", data={
        "name": "Тестовый жанр"
    })
    assert response.status_code == 400, f"Ожидался 400, но получен {response.status_code}"
    assert response.json()["error"] == "Такой жанр уже существует.", "Сообщение об ошибке должно быть 'Такой жанр уже существует.'" 

# тест на удаление не работает, не знаю как его написать (проблема: 35 строчка, связана с ручкой на удаление и её форматом)
@pytest.mark.asyncio
async def test_delete_genre(ac: AsyncClient):
    await ac.post("/api/v1/api/genres/add_genre", data={"name": "Тестовый жанр"})

    response = await ac.delete("/api/v1/api/genres/delete_genre",  data={"name": "Тестовый жанр"})

    assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code}"

    assert response.json()["message"] == "Жанр 'Тестовый жанр' успешно удален.", \
        f"Ожидалось сообщение 'Жанр 'Тестовый жанр' успешно удален.', но получено {response.json()['message']}"

