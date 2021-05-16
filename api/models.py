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
    sqlalchemy.Column("categorie", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("photos", postgresql.ARRAY(sqlalchemy.String), nullable=False),
    sqlalchemy.Column("price", sqlalchemy.Numeric, nullable=False),
    sqlalchemy.Column("promo_price", sqlalchemy.Numeric),
    sqlalchemy.Column("price_type", sqlalchemy.Enum(PriceType), nullable=False),
    sqlalchemy.Column("visibility", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("stock", sqlalchemy.Boolean, nullable=False, default=True),
)

contact = sqlalchemy.Table(
    "contact",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("address_city", sqlalchemy.String, nullable=False, server_default="B-5310 Leuze (Nam.)"),
    sqlalchemy.Column("address_street", sqlalchemy.String, nullable=False, server_default="Chaussée de Namur 301"),
    sqlalchemy.Column("email", sqlalchemy.String, nullable=False, server_default="info@boucherie-vangeebergen.be"),
    sqlalchemy.Column("facebook", sqlalchemy.String, nullable=False, server_default="https://www.facebook.com/boucherievangeebergen/"),
    sqlalchemy.Column("phone_mobile", sqlalchemy.String, nullable=False, server_default="0477 86 07 92"),
    sqlalchemy.Column("phone_office", sqlalchemy.String, nullable=False, server_default="081 40 06 16"),
    sqlalchemy.Column("tva", sqlalchemy.String, nullable=False, server_default="BE 0700.234.189"),
)
