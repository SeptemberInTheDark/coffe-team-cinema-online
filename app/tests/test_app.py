import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_app(ac: AsyncClient):
    response = await ac.get("/")
    assert response.status_code == 307, f"Ожидался 307(перенаправление на swagger), но получен {response.status_code}"
