from db import db, metadata
from db.sqlalchemy import Table, Column, Integer, String


""" EXAMPLE
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String),
    Column("last_name", String),
    Column("age", Integer),
)


class User:
    @classmethod
    async def get(cls, id):
        query = users.select().where(users.c.id == id)
        user = await db.fetch_one(query)
        return user

    @classmethod
    async def create(cls, **user):
        query = users.insert().values(**user)
        user_id = await db.execute(query)
        return user_id
"""
