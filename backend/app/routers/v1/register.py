
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.core.init_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession


from app.crud.crud_user import UserCRUD

from app.schemas.User import UserCreate
from app.utils.logging import AppLogger



logger = AppLogger().get_logger()


router = APIRouter()


@router.post("")
async def user_registration(

    userd_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    try:

        existing_user = await UserCRUD.check_user(db, userd_data.username, userd_data.email, userd_data.phone)
        if existing_user:
            return JSONResponse(status_code=400,
                                content={"error": "Пользователь с таким именем или почтой уже существует."})

        new_user = UserCreate(
            username=userd_data.username,
            email=userd_data.email,
            phone=userd_data.phone,
            hashed_password=userd_data.password,
        )
        user = await UserCRUD.create_user(db=db, user=new_user)

        if not user:
            return JSONResponse(status_code=400,
                                content={"error": "Ошибка при создании пользователя, попробуйте еще раз..."})
        logger.info(f"Пользователь {user.username} успешно зарегистрирован")

        return JSONResponse(status_code=201, content={
            "success": True,
            "message": "Пользователь успешно зарегистрирован",
            "data": {"user_id": user.id}
        })

    except Exception as exc:
        logger.error(f'Ошибка при создании пользователя: {exc}')
        return JSONResponse(status_code=500, content={"error": "Внутренняя ошибка сервера"})
