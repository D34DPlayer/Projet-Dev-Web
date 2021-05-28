from datetime import datetime
from typing import Optional

import sqlalchemy
from pydantic import BaseModel, Field
from pydantic.types import conint, constr
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from .db import db
from .models import PriceType, comments, contact, horaire, products, users


class PageModel(BaseModel):
    page: conint(ge=1) = 1
    size: conint(ge=1, le=100) = 50


class TokenModel(BaseModel):
    access_token: str
    token_type = "bearer"


class User(BaseModel):
    username: constr(max_length=15)
    email: Optional[constr(max_length=30)]


class CreateUser(User):
    password: str


class VisibilityModel(BaseModel):
    visibility: bool


class StockModel(BaseModel):
    stock: bool


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
    open: Optional[constr(regex=r"\d{1,2}:\d{2}")] = None
    close: Optional[constr(regex=r"\d{1,2}:\d{2}")] = None


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
    name: constr(max_length=50)
    categorie: constr(max_length=50)
    description: constr(max_length=5000)
    photos: list[str] = []
    price: float
    promo_price: float = None
    price_type: PriceType
    visibility: bool = False
    stock: bool = True

    @classmethod
    async def add(cls, product: "Product") -> "Product":
        values = product.dict()
        if product.id is None:
            values.pop("id")

        query = products.insert().values(**values)
        product.id = await db.execute(query)

        return product

    @classmethod
    async def find(cls, page: PageModel, **kwargs) -> "ListProduct":
        def escape(value: str) -> str:
            """Escape a value and add % to match any text before and after."""
            return "%" + value.replace("/", "//").replace("%", "/%") + "%"

        # Create a list of condition from the kwargs
        conditions = [getattr(products.c, field).like(escape(value), escape="/") for field, value in kwargs.items()]

        # Verify that the conditions are not empty
        if len(conditions) == 0:
            raise ValueError("You need to filter at least one field.")

        # Aggregate the conditions into a where clause
        condition = sqlalchemy.and_(*conditions)
        query = products.select().where(condition)
        total = await db.execute(select([func.count()]).select_from(products).where(condition))

        # Add limit and offset to the query
        query = query.offset((page.page - 1) * page.size).limit(page.size)
        return ListProduct(items=await db.fetch_all(query), total=total, page=page.page, size=page.size)

    @classmethod
    async def get(cls, id: int) -> Optional["Product"]:
        query = products.select().where(products.c.id == id)
        product = await db.fetch_one(query)
        if product:
            return Product(**product)

    @classmethod
    async def get_all(cls, page: PageModel) -> "ListProduct":
        query = products.select().order_by(products.c.id).offset((page.page - 1) * page.size).limit(page.size)
        total = await db.execute(select([func.count()]).select_from(products))

        return ListProduct(items=await db.fetch_all(query), total=total, page=page.page, size=page.size)

    @classmethod
    async def get_photos(cls, id: int) -> list[str]:
        query = select([products.c.photos]).where(products.c.id == id)
        return await db.execute(query)

    @classmethod
    async def update(cls, id: int, **kwargs) -> "Product":
        query = products.update().where(products.c.id == id).values(**kwargs).returning(products)
        product = await db.fetch_one(query)
        if product:
            return Product(**product)

    @classmethod
    async def edit(cls, id: int, product: "Product") -> "Product":
        product = product.dict()
        product.pop("id")
        return await cls.update(id, **product)

    @classmethod
    async def edit_photos(cls, id: int, new_photos: list[str]) -> list[str]:
        query = products.update().where(products.c.id == id).values(photos=new_photos)
        await db.execute(query)
        return new_photos

    @classmethod
    async def remove_photos(cls, id: int, to_remove: list[str]) -> Optional[list[str]]:
        photos = await Product.get_photos(id)

        if photos is not None:
            return await Product.edit_photos(id, [url for url in photos if url not in to_remove])

    @classmethod
    async def delete(cls, product_id: int) -> Optional["Product"]:
        product = await cls.get(product_id)
        if product:
            query = products.delete().where(products.c.id == product_id)
            await db.execute(query)

        return product

    @classmethod
    async def show(cls, id: int) -> Optional["Product"]:
        query = products.update().where(products.c.id == id).values(visibility=True).returning(products)
        product = await db.fetch_one(query)
        if product:
            return Product(**product)

    @classmethod
    async def hide(cls, id: int) -> Optional["Product"]:
        query = products.update().where(products.c.id == id).values(visibility=False).returning(products)
        product = await db.fetch_one(query)
        if product:
            return Product(**product)


class CommentBrief(BaseModel):
    id: Optional[int]
    name: constr(max_length=30)
    seen: Optional[bool] = False
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)


class Comment(CommentBrief):
    email: constr(max_length=30)
    comment: constr(max_length=5000)
    address: Optional[constr(max_length=100)]
    telephone: Optional[constr(max_length=20)]

    @classmethod
    async def get_all(cls):
        query = comments.select()
        return await db.fetch_all(query)

    @classmethod
    async def get(cls, id: int):
        query = comments.select().where(comments.c.id == id)
        comment = await db.fetch_one(query)
        if comment and not comment["seen"]:
            return await cls.change_seen(id, True)
        return comment or None

    @classmethod
    async def add(cls, comment):
        values = comment.dict()
        if comment.id is None:
            values.pop("id")

        query = comments.insert().values(**values)
        comment.id = await db.execute(query)

        return comment

    @classmethod
    async def delete(cls, id: int):
        old_comment = await cls.get(id)

        if old_comment:
            query = comments.delete().where(comments.c.id == id)
            await db.execute(query)

            return old_comment

    @classmethod
    async def change_seen(cls, id: int, seen: bool):
        query = comments.update().where(comments.c.id == id).values(seen=seen).returning(comments)
        comment = await db.fetch_one(query)
        if comment:
            return Comment(**comment)

    @classmethod
    async def change_list_seen(cls, ids: list[int], seen: bool) -> "list[Comment]":
        query = comments.update().where(comments.c.id.in_(ids)).values(seen=seen).returning(comments)
        print(query)
        return await db.fetch_all(query)

    @classmethod
    async def delete_list(cls, ids: list[int]) -> "list[Comment]":
        query = comments.delete().where(comments.c.id.in_(ids)).returning(comments)
        return await db.fetch_all(query)


class SeenModel(BaseModel):
    seen: bool
    comments: Optional[list[int]] = None


class DeleteListModel(BaseModel):
    ids: list[int]


class ListProduct(PageModel):
    total: int
    items: list[Product]


class Address(BaseModel):
    city: str
    street: str


class Phone(BaseModel):
    mobile: str
    office: str


class Contact(BaseModel):
    address: Address
    email: str
    facebook: str
    phone: Phone
    tva: str

    @classmethod
    async def get(cls) -> "Contact":
        """Get the contact informations from hte database. If it doesn't exists yet, it will insert default values."""
        data = await db.fetch_one(contact.select())
        if data is None:
            # Insert default values
            # Currently it's not possible with sqlalchemy
            # And we use "returning" to return the inserted values.
            data = await db.fetch_one("INSERT INTO contact DEFAULT VALUES RETURNING *")

        # Convert it to a dictionary
        data = dict(data)
        # Then convert address_* to an object
        data["address"] = Address(city=data.pop("address_city"), street=data.pop("address_street"))
        # Do the same for phon_*
        data["phone"] = Phone(mobile=data.pop("phone_mobile"), office=data.pop("phone_office"))
        # And return this contact
        return Contact(**data)

    @classmethod
    async def edit(cls, c: "Contact") -> "Contact":
        """Edit the contact informations."""
        # Convert the contact to a dictionary
        values = c.dict()
        # Remove address and phone from the values
        values.pop("address")
        values.pop("phone")

        # Convert the address and phone numbers to  flat data
        values.update(
            {
                "id": 1,  # Update the unique row
                "address_city": c.address.city,
                "address_street": c.address.street,
                "phone_mobile": c.phone.mobile,
                "phone_office": c.phone.office,
            }
        )

        # Execute the query and return the inserted values
        await db.execute(contact.update().values(**values))
        return await cls.get()
