from pydantic import BaseModel
from typing import Optional

from .db import db
from .models import users


class TokenModel(BaseModel):
    access_token: str
    token_type = "bearer"


class User(BaseModel):
    username: str
    email: Optional[str]


class CreateUser(User):
    password: str


class DBUser(User):
    hashed_password: str

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
    async def update(cls, username: str, user):
        old_user = await cls.get(username)
        if old_user:
            query = users.update().where(users.c.username == username).values(**user.dict())
            await db.execute(query)
            return user

    @classmethod
    async def delete(cls, username: str):
        user = await cls.get(username)
        if user:
            query = users.delete().where(users.c.username == username)
            await db.execute(query)
        return user

    @classmethod
    async def get_all(cls):
        query = users.select()

        return await db.fetch_all(query)
