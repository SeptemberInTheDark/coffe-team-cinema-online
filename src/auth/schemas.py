from pydantic import BaseModel


class User(BaseModel):
    username: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None


class UserInDB(User):
    hashed_password: str
