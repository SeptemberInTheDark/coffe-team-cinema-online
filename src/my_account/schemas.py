from pydantic import BaseModel
from typing import Optional, List


class UserData(BaseModel):
    id: int
    username: Optional[str] = None
    links: Optional[List[str]] = []
    sex: Optional[str] = None
    age: Optional[int] = None
    country: Optional[str] = None
    town: Optional[str] = None
    love_genres: Optional[List[str]] = []
    avatar: Optional[str] = None #base64
    comments: Optional[List[str]] = []
