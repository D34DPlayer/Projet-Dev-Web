import sys

import pytest

from api.db import db as database

sys.path.append('/')

from api.schemas import DBUser


@pytest.fixture
async def db():
    await database.connect()
    yield database
    await database.disconnect()


class TestDBUser:
    user = DBUser(username="carlos", hashed_password="viandehachée", email=None)

    @pytest.mark.asyncio
    async def test_create(self, db):
        user = await DBUser.create(self.user)
        assert user == self.user

        user = await DBUser.create(self.user)
        assert user is None

    @pytest.mark.asyncio
    async def test_get(self, db):
        await DBUser.create(self.user)

        user = await DBUser.get(self.user.username)
        assert user == self.user
