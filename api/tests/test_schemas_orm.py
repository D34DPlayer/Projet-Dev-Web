import pytest

from api.db import db as database
from api.schemas import DBUser, Horaire, Product


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


class TestProduct:
    product = Product(
        name="Viande",
        categorie="Casher",
        description="Ceci est très sympa",
        price=1.32,
        price_type="/kilo",
        visibility=True
    )
    photos = ["/images/viande.png", "/images/poulet.png"]

    @pytest.mark.asyncio
    async def test_add(self, db):
        """TO DO: Test add method"""
        product = await Product.add(self.product)
        assert product.id is not None
        assert product == self.product

    @pytest.mark.asyncio
    async def test_get(self, db):
        """TO DO: Test get method"""

    @pytest.mark.asyncio
    async def test_get_all(self, db):
        """TO DO: Test get_all method"""

    @pytest.mark.asyncio
    async def test_edit_photos(self, db):
        """TO DO: Test edit_photos method"""
        photos = await Product.edit_photos(1, self.photos)
        assert photos == self.photos

    @pytest.mark.asyncio
    async def test_get_photos(self, db):
        """TO DO: Test get_photos method"""
        photos = await Product.get_photos(1)
        assert photos == self.photos

    @pytest.mark.asyncio
    async def test_remove_photos(self, db):
        remove_photos = await Product.remove_photos(1, ["/images/viande.png"])
        photos = await Product.get_photos(1)

        assert len(photos) == len(remove_photos) == 1
        assert "/images/poulet.png" in photos
        assert "/images/poulet.png" in remove_photos

        remove_photos = await Product.remove_photos(1, ["/images/poulet.png"])

        assert len(remove_photos) == 0

    @pytest.mark.asyncio
    async def test_delete(self, db):
        removed_product = await Product.delete(1)
        fake_product = await Product.delete(69)

        assert fake_product is None
        assert removed_product == self.product

        product = await Product.get(1)

        assert product is None

    @pytest.mark.asyncio
    async def test_edit(self, db):
        """TO DO: Test edit method"""

    @pytest.mark.asyncio
    async def test_show(self, db):
        """TO DO: Test show method"""

    @pytest.mark.asyncio
    async def test_hide(self, db):
        """TO DO: Test hide method"""
