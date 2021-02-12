import os
from databases import Database
import sqlalchemy


db = Database(os.environ["DATABASE_URL"])

metadata = sqlalchemy.MetaData()
