from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    username: str
    email: str
    phone: str
    hashed_password: str

    is_active: Optional[bool] = True


class UserCreate(User):
    username: str
    hashed_password: str
    phone: str
    email: str

    class Config:
        from_attributes = True
