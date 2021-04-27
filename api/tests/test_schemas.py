import sys

from pydantic import ValidationError
import pytest

sys.path.append('/')

import api.schemas as sch


class BaseModelTest:
    correct_data = {}
    wrong_data = []
    irregular_data = []

    def test_validate(self):
        assert sch.TokenModel(**self.correct_data) == self.correct_data

        for wrong in self.wrong_data:
            with pytest.raises(ValidationError):
                sch.TokenModel(**wrong)

    def test_parsing(self):
        for irregular in self.irregular_data:
            assert sch.TokenModel(**irregular) == self.correct_data


class TestTokenModel(BaseModelTest):
    correct_data = {"access_token": "ceciestuntoken", "token_type": "bearer"}
    wrong_data = [{"no_access_token": "ceciestuntoken"}]
    irregular_data = [{"access_token": "ceciestuntoken", "token_type": "bearer", "extra": "extra"},
                      {"access_token": "ceciestuntoken"}]
