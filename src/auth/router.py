from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .schemas import User
from db import get_db
from src.Users.crud import UserCRUD
from sqlalchemy.ext.asyncio import AsyncSession
import os
from src.Users.manager import UserHashManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix='/api',
    tags=['Авторизация'],
)


async def decode_token(token, db: AsyncSession = Depends(get_db)):
    # This doesn't provide any security at all
    # Check the next version
    user = await UserCRUD.get_user(db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = await UserCRUD.get_users.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = User(**user_dict)
    user_salt = os.urandom(32).hex()
    hashed_password = UserHashManager.hash_str(form_data.password, user_salt)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}
