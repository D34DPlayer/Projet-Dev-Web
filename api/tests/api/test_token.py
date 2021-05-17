from datetime import timedelta

from fastapi import status
from fastapi.testclient import TestClient

from api.app import create_access_token


class TestHelloWorld:
    def test_hello_world(self, client: TestClient):
        # Make sure we greet anyone passing by
        response = client.get('/')
        assert response.json() == {"message": "Hello World"}


class TestToken:
    form = {
        "grant_type": "",
        "client_id": "",
        "client_secret": "",
        "username": "admin",
        "password": "superpassword"
    }

    def test_incorrect_password(self, client: TestClient):
        # Try using an incorrect password
        form = self.form.copy()
        form['password'] = 'incorrect'

        # It should reply with a 401 error
        response = client.post("/token", data=form)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_garbage_token(self, client: TestClient):
        # Craft an invalid token
        headers = {
            "Authorization": "Bearer craftedtoken"
        }

        # It should return a 401 error
        response = client.get('/users/me', headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_missing_user(self, client: TestClient):
        # Create a valid access token with a invalid user.
        headers = {
            "Authorization": "Bearer " + create_access_token(dict(sub="i do not exist"))
        }

        # Since the user doesn't exists anymore, it should return a 401 error.
        response = client.get('/users/me', headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_expired_token(self, client: TestClient):
        # Create a valid but expired access token.
        headers = {
            "Authorization": "Bearer " + create_access_token(dict(sub="admin"), timedelta(minutes=-1))
        }

        # Since it's not valid anymore, it should return a 401 error.
        response = client.get('/users/me', headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_crafted_payload(self, client: TestClient):
        # Create a valid token without payload.
        headers = {
            "Authorization": "Bearer " + create_access_token({})
        }

        # It should return a 401 error.
        response = client.get('/users/me', headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_correct_token(self, client: TestClient):
        # Try using the correct password
        response = client.post("/token", data=self.form)
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('access_token') is not None
        assert response.json().get('token_type') == 'bearer'

        headers = {
            "Authorization": "Bearer " + response.json()['access_token']
        }

        # Check that the given token is working
        response = client.get('/users/me', headers=headers)
        assert response.status_code == status.HTTP_200_OK
