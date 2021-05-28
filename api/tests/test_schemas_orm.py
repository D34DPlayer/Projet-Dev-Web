import pytest

from api.db import db as database
from api.schemas import DBUser, Horaire, PageModel, Product


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
        visibility=True,
        stock=True,
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
        """Test get method"""
        product_get = await Product.get(1)
        assert product_get == self.product

        product_get = await Product.get(666)
        assert product_get is None

    @pytest.mark.asyncio
    async def test_get_all(self, db):
        """Test get_all method"""
        all_product = await Product.get_all(PageModel(size=24))
        assert all_product.page == 1
        assert all_product.size == 24
        assert all_product.total == 1
        assert all_product.items == [self.product]

        all_product = await Product.get_all(PageModel(page=2, size=24))
        assert all_product.page == 2
        assert all_product.size == 24
        assert all_product.total == 1
        assert all_product.items == []

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
    async def test_update(self, db):
        product = await Product.update(1, name="test")
        assert product.name == "test"

        product = await Product.edit(1, self.product)
        assert product == self.product

    @pytest.mark.asyncio
    async def test_hide(self, db):
        """TO DO: Test hide method"""
        Product_hide = await Product.hide(1)
        assert not Product_hide.visibility

        Product_hide = await Product.hide(666)
        assert Product_hide is None

    @pytest.mark.asyncio
    async def test_show(self, db):
        """TO DO: Test show method"""
        Product_show = await Product.show(1)
        assert Product_show == self.product
        assert Product_show.visibility

        Product_show = await Product.show(666)
        assert Product_show is None

    @pytest.mark.asyncio
    async def test_delete(self, db):
        removed_product = await Product.delete(1)
        fake_product = await Product.delete(69)

        assert fake_product is None
        assert removed_product == self.product

        product = await Product.get(1)

        assert product is None
