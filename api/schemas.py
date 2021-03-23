from pydantic import BaseModel
from typing import Optional

from .db import db
from .models import users


class User(BaseModel):
    username: str
    email: Optional[str]


class CreateUser(User):
    password: str


class DBUser(User):
    hashed_password: str

    class Config:
        orm_mode = True
        
    @classmethod
    async def get(cls, username: str):
        query = users.select().where(users.c.username == username)
        user = await db.fetch_one(query)
        if user:
            return DBUser(**user)

    @classmethod
    async def create(cls, user):
        query = users.insert().values(**user.dict())
        await db.execute(query)
        return user

    @classmethod
    async def update(cls, user):
        old_user = await cls.get(user.username)
        if old_user:
            query = users.update().where(users.c.username == user.username).values(**user.dict())
            await db.execute(query)
            return user

    @classmethod
    async def delete(cls, username: str):
        user = await cls.get(username)
        if user:
            query = users.delete().where(users.c.username == username)
            await db.execute(query)
        return user
