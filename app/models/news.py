from sqlalchemy import Column, Integer, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR

from app.core.init_db import BaseModel


class NewsActor(BaseModel):
    __tablename__ = "news_actor"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("public.user.id"), nullable=False)
    news_id = Column(Integer, ForeignKey("public.news.id"), nullable=False)


class NewsViews(BaseModel):
    __tablename__ = "news_views"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("public.user.id"), nullable=False)
    news_id = Column(Integer, ForeignKey("public.news.id"), nullable=False)
    is_view = Column(Boolean, default=False)


class NewsComments(BaseModel):
    __tablename__ = "news_comments"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("public.user.id"), nullable=False)
    news_id = Column(Integer, ForeignKey("public.news.id"), nullable=False)
    text_comment = Column(Text, nullable=False)


class News(BaseModel):
    __tablename__ = "news"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR(length=50), nullable=False)
    sub_title = Column(VARCHAR(length=255), nullable=True)
    text_news = Column(Text, nullable=True)
    comment = Column(Integer, nullable=True)
    source = Column(VARCHAR(length=255), nullable=True)




#test

