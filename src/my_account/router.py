from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserData, DeleteResponse, UserSettings


router = APIRouter(
    prefix='/api',
    tags=['Личный кабинет'],
)


user_list = [
    {
        "id": 1,
        "username": 'User98767',
        "first_name": None,
        "last_name": None,
        "links": ["https://facebook/a2342fsdf/"],
        "sex": "Мужской",
        "age": 26,
        "country": None,
        "town": None,
        "love_genres": [],
        "avatar": None,
        "comments": [],
        "info": []
    },
    {
        "id": 2,
        "username": 'Sentiago',
        "first_name": "Andrey",
        "last_name": "Kolalev",
        "links": [],
        "sex": "Мужской",
        "age": 38,
        "country": "Australia",
        "town": None,
        "love_genres": ["trillers"],
        "avatar": None,
        "comments": [],
        "info": []
    },
]


@router.get('/me/{id}', response_model=UserData)
async def my_account(id: int, db: AsyncSession = Depends(get_db)):
    user = next((user for user in user_list if user['id'] == id), None)
    if user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return UserData(**user)


@router.delete('/me/{id}', response_model=DeleteResponse)
async def delete_account(id: int, db: AsyncSession = Depends(get_db)):
    user_to_del = next((user for user in user_list if user['id'] == id), None)

    if user_to_del is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    user_list.remove(user_to_del)
    return DeleteResponse(id=id)


@router.put('/me/{id}/settings/', response_model=UserData)
async def change_data_account(id: int, data: UserSettings, db: AsyncSession = Depends(get_db)):
    user = next((user for user in user_list if user['id'] == id), None)
    if user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    for key, value in data.model_dump(exclude_unset=True).items():
        user[key] = value

    return UserData(**user)
