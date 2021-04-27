import sys

import pytest
from pydantic import ValidationError

from api import schemas as sch


class BaseModelTest:
    schema = None
    correct_data = {}
    wrong_data = []
    irregular_data = []

    def test_validate(self):
        assert self.schema(**self.correct_data) == self.correct_data

        for wrong in self.wrong_data:
            with pytest.raises(ValidationError):
                self.schema(**wrong)

    def test_parsing(self):
        for irregular in self.irregular_data:
            assert self.schema(**irregular) == self.correct_data


class TestTokenModel(BaseModelTest):
    schema = sch.TokenModel
    correct_data = {"access_token": "ceciestuntoken", "token_type": "bearer"}
    wrong_data = [{"no_access_token": "ceciestuntoken"}]
    irregular_data = [{"access_token": "ceciestuntoken", "token_type": "bearer", "extra": "extra"},
                      {"access_token": "ceciestuntoken"}]


class TestUser(BaseModelTest):
    schema = sch.User
    correct_data = {"username": "cyril", "email": "toto@gmail.com"}
    wrong_data = [{"usernameu": "cyril"}, {"emaile": "toto@gmail.com"}]
    irregular_data = [{"username": "cyril", "email": "toto@gmail.com", "extra": "extra"}]


class TestCreateUser(BaseModelTest):
    schema = sch.CreateUser
    correct_data = {"username": "cyril", "password": "mdp", "email": None}
    wrong_data = [{"usernameu": "cyril", "password": "mdp"}, {"username": "cyril", "passworde": "mdp"}]
    irregular_data = [{"username": "cyril", "password": "mdp", "email": None, "extra": "extra"},
                      {"username": "cyril", "password": "mdp"}]


class TestVisibilityModel(BaseModelTest):
    schema = sch.VisibilityModel
    correct_data = {"visibility": False}
    wrong_data = [{"visibilitie": False}]
    irregular_data = [{"visibility": False, "extra": "extra"},
                      {"visibility": "False"}, {"visibility": "false"}, {"visibility": 0}, {"visibility": "0"}]


class TestDBUser(BaseModelTest):
    schema = sch.DBUser
    correct_data = {"username": "cyril", "hashed_password": "mdphash", "email": None}
    wrong_data = [{"usernameu": "cyril", "hashed_password": "mdphash"},
                  {"username": "cyril", "hashed_passworde": "mdphash"}]
    irregular_data = [{"username": "cyril", "hashed_password": "mdphash", "email": None, "extra": "extra"},
                      {"username": "cyril", "hashed_password": "mdphash"}]


class TestDayHoraire(BaseModelTest):
    schema = sch.DayHoraire
    correct_data = {"is_open": True, "open": "00:30:00", "close": "03:32:00"}
    wrong_data = []
    irregular_data = [{"is_open": "true", "open": "00:30:00", "close": "03:32:00"},
                      {"is_open": "true", "open": "00:30:00", "close": "03:32:00", "extra": "extra"}]


class TestHoraire(BaseModelTest):
    schema = sch.Horaire
    correct_data = {
        "lu": {
            "is_open": False, "open": None, "close": None
        },
        "ma": {
            "is_open": True, "open": "00:00:00", "close": "10:00:30"
        },
        "me": {
            "is_open": False, "open": None, "close": None
        },
        "je": {
            "is_open": False, "open": None, "close": None
        },
        "ve": {
            "is_open": False, "open": None, "close": None
        },
        "sa": {
            "is_open": False, "open": None, "close": None
        },
        "di": {
            "is_open": False, "open": None, "close": None
        },
    }
    wrong_data = []
    irregular_data = [{
        "ma": {
            "is_open": True, "open": "00:00:00", "close": "10:00:30"
        },
    }]


class TestProduct(BaseModelTest):
    schema = sch.Product
    correct_data = {
        "id": 3, "name": "Viande", "categorie": "truc",
        "description": "ceciestunedescription", "photos": ["/img1", "/img2"],
        "price": 12.56, "promo_price": None,
        "price_type": "/kilo", "visibility": False
    }
    wrong_data = [{
        "id": 3, "name": "Viande", "categorie": "truc",
        "description": "ceciestunedescription", "photos": ["/img1", "/img2"],
        "price": "prix", "promo_price": None,
        "price_type": "/kilo", "visibility": False
    }, {
        "id": 3, "nameu": "Viande", "categorie": "truc",
        "description": "ceciestunedescription", "photos": ["/img1", "/img2"],
        "price": 12.56, "promo_price": None,
        "price_type": "/kilo", "visibility": False
    }]
    irregular_data = [{
        "id": 3, "name": "Viande", "categorie": "truc",
        "description": "ceciestunedescription", "photos": ["/img1", "/img2"],
        "price": 12.56, "price_type": "/kilo", "visibility": False
    }, {
        "id": 3, "name": "Viande", "categorie": "truc",
        "description": "ceciestunedescription", "photos": ["/img1", "/img2"],
        "price": 12.56, "promo_price": None,
        "price_type": "/kilo"
    }, {
        "id": 3, "name": "Viande", "categorie": "truc",
        "description": "ceciestunedescription", "photos": ["/img1", "/img2"],
        "price": 12.56, "promo_price": None,
        "price_type": "/kilo", "visibility": False, "extra": "extra"
    }]
