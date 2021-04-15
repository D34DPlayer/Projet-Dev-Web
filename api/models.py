from api.db import metadata
from api.db import sqlalchemy

import enum
from sqlalchemy.dialects import postgresql


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

