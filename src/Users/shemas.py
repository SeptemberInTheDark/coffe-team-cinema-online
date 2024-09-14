from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    phone: str



class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    first_name: str
    last_name: str
    is_active: bool
