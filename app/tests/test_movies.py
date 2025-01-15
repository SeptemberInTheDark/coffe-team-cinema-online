from httpx import AsyncClient


async def test_add_movie(ac: AsyncClient):
    await ac.post("/api/genres/add_genre", data={
        "name": "Жанр Один"
    })
    response = await ac.post("/api/movies/add_movie", data={
        "title": "Тестовый фильм",
        "url_movie": "http://example.com/test-movie",
        "description": "Описание тестового фильма.",
        "photo": "http://example.com/photo.jpg",
        "release_year": 2024,
        "director": "Тестовый режиссер",
        "actors": ["Актер Один", "Актер Два"],  # Убедитесь, что это корректно обрабатывается
        "duration": 120,
        "genre_name": "Жанр Один"
    })
    
    print(response.text)  # Выводим текст ответа для отладки
    assert response.status_code == 201, f"Ожидался 201, но получен {response.status_code}"

    
    # Проверяем содержимое ответа
    print(response.text)  # Выводим текст ответа для отладки


async def test_search_movies_by_title_and_description(ac: AsyncClient):
    response = await ac.get("/api/movies/search_movies_by_title_and_description", params={"query": "Тест"})
    assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code}"


async def test_search_movies_by_genre(ac: AsyncClient):
    response = await ac.get("/api/movies/search_movies_by_genre", params={"genre": "Жанр Один"})
    assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code}"
