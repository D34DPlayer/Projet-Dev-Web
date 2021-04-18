from api.db import metadata
from api.db import sqlalchemy

from enum import Enum
from sqlalchemy.dialects import postgresql


class PriceType(str, Enum):
    kilo = "/kilo"
    unite = "/unité"


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("hashed_password", sqlalchemy.String, nullable=False),
)

horaire = sqlalchemy.Table(
    "horaire",
    metadata,
    sqlalchemy.Column("day", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("is_open", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("open", sqlalchemy.String),
    sqlalchemy.Column("close", sqlalchemy.String),
)

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("photos", postgresql.ARRAY(sqlalchemy.String), nullable=False),
    sqlalchemy.Column("price", sqlalchemy.Numeric, nullable=False),
    sqlalchemy.Column("promo_price", sqlalchemy.Numeric),
    sqlalchemy.Column("price_type", sqlalchemy.Enum(PriceType), nullable=False),
    sqlalchemy.Column("visibility", sqlalchemy.Boolean, nullable=False),
)
