from pydantic import BaseModel, Field
from typing import Optional, List, Literal


class UserData(BaseModel):
    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    links: Optional[List[str]] = None
    sex: Optional[Literal["Мужской", "Женский"]] = None
    age: Optional[int] = Field(None, ge=0, le=120)
    country: Optional[str] = None
    town: Optional[str] = None
    love_genres: Optional[List[str]] = None
    avatar: Optional[str] = None #base64
    comments: Optional[List[str]] = None
    info: Optional[List[str]] = None


class DeleteResponse(BaseModel):
    id: int


class UserSettings(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    links: Optional[List[str]] = None
    sex: Optional[Literal["Мужской", "Женский"]] = None
    age: Optional[int] = Field(None, ge=0, le=120)
    country: Optional[str] = None
    town: Optional[str] = None
    love_genres: Optional[List[str]] = None
    info: Optional[List[str]] = None
