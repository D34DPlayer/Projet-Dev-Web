import sys

import pytest

from api.db import db as database

sys.path.append('/')

from api.schemas import DBUser, Horaire


@pytest.fixture
async def db():
    await database.connect()
    yield database
    await database.disconnect()


@pytest.mark.asyncio
async def test_db_connection():
    await database.connect()
    await database.disconnect()


class TestDBUser:
    user = DBUser(username="carlos", hashed_password="viandehachée", email=None)
    modified_user = DBUser(username="carlos", hashed_password="viandehachée", email="outlook")
    user2 = DBUser(username="michmich", hashed_password="chevaldetroie", email=None)

    @pytest.mark.asyncio
    async def test_create(self, db):
        user = await DBUser.create(self.user)
        assert user == self.user

        user = await DBUser.create(self.user)
        assert user is None

    @pytest.mark.asyncio
    async def test_get(self, db):
        user = await DBUser.get(self.user.username)
        assert user == self.user

    @pytest.mark.asyncio
    async def test_update(self, db):
        user = await DBUser.update(self.user.username, self.modified_user)
        assert user == self.modified_user

        user = await DBUser.get(self.modified_user.username)
        assert user == self.modified_user

        user = await DBUser.get(self.user.username)
        assert user != self.user

    @pytest.mark.asyncio
    async def test_delete(self, db):
        user = await DBUser.get(self.modified_user.username)
        assert user == self.modified_user

        await DBUser.delete(self.modified_user.username)

        user = await DBUser.get(self.modified_user.username)
        assert user is None

    @pytest.mark.asyncio
    async def test_get_all(self, db):
        await DBUser.create(self.user2)

        users = await DBUser.get_all()

        assert len(users) == 2


class TestHoraire:
    default_horaire = Horaire()
    horaire = Horaire(ma={"is_open": True, "open": "00:00:00", "close": "10:00:30"})

    @pytest.mark.asyncio
    async def test_get(self, db):
        horaire = await Horaire.get()
        assert horaire == self.default_horaire

    @pytest.mark.asyncio
    async def test_edit(self, db):
        horaire = await Horaire.edit(self.horaire)
        assert horaire == self.horaire

        horaire = await Horaire.get()
        assert horaire == self.horaire
