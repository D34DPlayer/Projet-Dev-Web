from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from .db import db
from .models import PriceType, horaire, products, users


class TokenModel(BaseModel):
    access_token: str
    token_type = "bearer"


class User(BaseModel):
    username: str
    email: Optional[str]


class CreateUser(User):
    password: str


class VisibilityModel(BaseModel):
    visibility: bool


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
        old_user = await cls.get(user.username)
        if not old_user:
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


class DayHoraire(BaseModel):
    is_open: bool = False
    open: Optional[str] = None
    close: Optional[str] = None


class Horaire(BaseModel):
    lu: DayHoraire = DayHoraire()
    ma: DayHoraire = DayHoraire()
    me: DayHoraire = DayHoraire()
    je: DayHoraire = DayHoraire()
    ve: DayHoraire = DayHoraire()
    sa: DayHoraire = DayHoraire()
    di: DayHoraire = DayHoraire()

    @classmethod
    async def get(cls):
        query = horaire.select()
        reply = {}

        async for row in db.iterate(query=query):
            reply[row["day"]] = {**row}

        return Horaire(**reply)

    @classmethod
    async def edit(cls, data):
        for [key, val] in data.dict().items():
            query = insert(horaire).values(day=key, **val).on_conflict_do_update(index_elements=["day"], set_=val)
            await db.execute(query)
        return data


class Product(BaseModel):
    id: Optional[int]
    name: str
    categorie: str
    description: str
    photos: list[str] = []
    price: float
    promo_price: float = None
    price_type: PriceType
    visibility: bool = False

    @classmethod
    async def add(cls, product: 'Product') -> 'Product':
        values = product.dict()
        if product.id is None:
            values.pop('id')

        query = products.insert().values(**values)
        product.id = await db.execute(query)

        return product

    # @classmethod
    # async def find(cls, id: Filter['Product']) -> list['Product']:
    #     pass

    @classmethod
    async def get(cls, id: int) -> Optional['Product']:
        query = products.select().where(products.c.id == id)
        product = await db.fetch_one(query)
        if product:
            return Product(**product)

    @classmethod
    async def get_all(cls) -> list['Product']:
        query = products.select()
        return await db.fetch_all(query)

    @classmethod
    async def get_photos(cls, id: int) -> list[str]:
        query = select([products.c.photos]).where(products.c.id == id)
        return await db.execute(query)

    @classmethod
    async def edit_photos(cls, id: int, new_photos: list[str]) -> list[str]:
        query = products.update().where(products.c.id == id).values(photos=new_photos)
        await db.execute(query)
        return new_photos

    @classmethod
    async def remove_photos(cls, id: int, to_remove: list[str]) -> Optional[list[str]]:
        photos = await Product.get_photos(id)

        if photos is None:
            return None

        return await Product.edit_photos(id, [url for url in photos if url not in to_remove])

    @classmethod
    async def delete(cls, product_id: int) -> Optional['Product']:
        product = await cls.get(product_id)
        if product:
            query = products.delete().where(products.c.id == product_id)
            await db.execute(query)

        return product

    @classmethod
    async def edit(cls, id: int, product: 'Product') -> 'Product':
        pass

    @classmethod
    async def show(cls, id: int) -> Optional['Product']:
        query = products.update().where(products.c.id == id).values(visibility=True)
        await db.execute(query)
        return await cls.get(id)

    @classmethod
    async def hide(cls, id: int) -> Optional['Product']:
        query = products.update().where(products.c.id == id).values(visibility=False)
        await db.execute(query)
        return await cls.get(id)
