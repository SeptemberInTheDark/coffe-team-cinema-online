import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.testing.suite.test_reflection import users

from app.models.user import Role
from conftest import async_session_maker

from sqlalchemy import delete
from app.models.user import User

@pytest.fixture(autouse=True)
async def clear_users():
    async with async_session_maker() as session:
        await session.execute(delete(User))
        await session.commit()

# class Role(BaseModel):
#     __tablename__ = "role"
#     __table_args__ = {"schema": "public"}
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(VARCHAR(length=50), nullable=False)
#     permissions = Column(JSON, nullable=True)

@pytest.mark.asyncio
async def test_create_role():
    async with async_session_maker() as session:
        stmt = insert(Role).values(id=2, name='user')
        await session.execute(stmt)
        await session.commit()

        query = select(Role)
        result = await session.execute(query)
        roles = result.scalars().all()
        assert len(roles) == 1, "Должна быть одна запись в таблице Role"
        role = roles[0]
        assert role.id == 2, f"Ожидался id=2, но получен id={role.id}"
        assert role.name == 'user'


@pytest.mark.asyncio
async def test_user_registration(ac: AsyncClient):
    response = await ac.post("/api/v1/register", data={
        "username": "test",
        "password": "test",
        "email": "test@test.com",
        "phone": "79999999999",
    })
    assert response.status_code == 201, f"Ожидался 201, но получен {response.status_code}"


@pytest.mark.asyncio
async def test_get_all_users(ac: AsyncClient):
    response = await ac.post("/api/v1/register", data={
        "username": "test",
        "password": "test",
        "email": "test@test.com",
        "phone": "79999999999",
    })

    response = await ac.get("/api/v1/users")
    assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code}"


@pytest.mark.asyncio
async def test_get_current_user_by_email(ac: AsyncClient):
    response = await ac.post("/api/v1/register", data={
        "username": "test",
        "password": "test",
        "email": "test@test.com",
        "phone": "79999999999",
    })
    response = await ac.get("/api/v1/users/user/by_email/test@test.com")
    assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code}."
    user_email = response.json()
    assert user_email["user"]["login"] == "test", \
        f"Ожидался username = test, но получен username={user_email['user']['login']}"
    assert user_email["user"]["email"] == "test@test.com", \
        f"Ожидался email = test@test.com, но получен email={user_email['user']['email']}"
    assert user_email["user"]["phone"] == "79999999999", \
        f"Ожидался phone = 79999999999, но получен phone={user_email['user']['phone']}"
    async with async_session_maker() as session:
        await session.execute(delete(User).where(User.username == "test"))
        await session.commit()

@pytest.mark.asyncio
async def test_get_current_user_by_phone(ac: AsyncClient):
    response = await ac.post("/api/v1/register", data={
        "username": "test",
        "password": "test",
        "email": "test@test.com",
        "phone": "79999999999",
    })

    response = await ac.get("/api/v1/users/user/by_phone/79999999999")
    assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code}."
    user_phone = response.json()
    assert user_phone["user"]["login"] == "test", \
        f"Ожидался username = test, но получен username={user_phone['user']['login']}"
    assert user_phone["user"]["email"] == "test@test.com", \
        f"Ожидался email = test@test.com, но получен email={user_phone['user']['email']}"
    assert user_phone["user"]["phone"] == "79999999999", \
        f"Ожидался phone = 79999999999, но получен phone={user_phone['user']['phone']}"
    async with async_session_maker() as session:
        await session.execute(delete(User).where(User.username == "test"))
        await session.commit()

@pytest.mark.asyncio
async def test_get_current_user_by_login(ac: AsyncClient):
    response = await ac.post("/api/v1/register", data={
        "username": "test",
        "password": "test",
        "email": "test@test.com",
        "phone": "79999999999",
    })

    response = await ac.get("/api/v1/users/user/by_login/test")
    assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code}."
    user_login = response.json()
    assert user_login["user"]["login"] == "test", \
        f"Ожидался username = test, но получен username={user_login['user']['login']}"
    assert user_login["user"]["email"] == "test@test.com", \
        f"Ожидался email = test@test.com, но получен email={user_login['user']['email']}"
    assert user_login["user"]["phone"] == "79999999999", \
        f"Ожидался phone = 79999999999, но получен phone={user_login['user']['phone']}"
    async with async_session_maker() as session:
        await session.execute(delete(User).where(User.username == "test"))
        await session.commit()