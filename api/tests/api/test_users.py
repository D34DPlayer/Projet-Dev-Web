from api.schemas import User
from api.app import create_access_token
from fastapi import status
from fastapi.testclient import TestClient


class TestUsers:
    user = User(username="test", email="test@example.com")
    token = "Bearer " + create_access_token({"sub": user.username})
    headers = dict(Authorization=token)

    def test_list_users(self, client: TestClient, headers: dict):
        # Check for authorizations
        response = client.get("/users")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # By default, the database is created with one user: admin.
        # Listing the users should return only this default admin.
        response = client.get("/users", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list) and len(response.json())
        assert response.json()[0].get("username") == "admin"

    def test_add_user(self, client: TestClient, headers: dict):
        user = self.user.dict()
        user["password"] = "password"

        # Check for authorizations
        response = client.post("/users", json=user)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Add a new user to the database.
        response = client.post("/users", json=user, headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.user

        # Add a same user again. You cannot create two users with the same name.
        response = client.post("/users", json=user, headers=headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_user(self, client: TestClient):
        # Check for authorizations
        response = client.get(f"/users/{self.user.username}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Check that the user added in the previous test is really added.
        response = client.get(f"/users/{self.user.username}", headers=self.headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.user

        # The api should return a 404 error if the user doesn't exist.
        response = client.get("/users/michel", headers=self.headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_me(self, client: TestClient):
        # Check for authorizations
        response = client.get("/users/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Check that the token return the correct user.
        response = client.get("/users/me", headers=self.headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.user

    def test_update_user(self, client: TestClient):
        user = self.user.dict()
        user["password"] = "anotherpassword"

        # Check for authorizations
        response = client.put(f"/users/{self.user.username}", json=user)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Update an user that doesn't exist. It should return a 404 error.
        response = client.put("/users/michel", json=user, headers=self.headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Update the user's password.
        response = client.put(f"/users/{self.user.username}", json=user, headers=self.headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.user

    def test_delete_user(self, client: TestClient, headers):
        # Check for authorizations
        response = client.delete(f"/users/{self.user.username}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Deleting ourself is not be possible.
        response = client.delete(f"/users/{self.user.username}", headers=self.headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Deleting a user that doesn't exist should return a 404 error.
        response = client.delete("/users/michel", headers=self.headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Delete the test user.
        response = client.delete(f"/users/{self.user.username}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.user

        # It should be gone
        response = client.get(f"/users/{self.user.username}", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
