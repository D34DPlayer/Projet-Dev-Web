from fastapi import status
from fastapi.testclient import TestClient

from api.schemas import Address, Contact, Phone


class TestContact:
    contact = Contact(
        address=Address(city="Pécrot", street="Rue machin"),
        phone=Phone(mobile="555 06 90 12", office="010 23 23 23"),
        email="test@boucherie.tk",
        facebook="https://www.facebook.com/boucherie",
        tva="BE 57 01 35 42",
    )

    def test_get_contact(self, client: TestClient):
        # Get contact informations. It should have the default values
        response = client.get("/contact")
        assert response.status_code == status.HTTP_200_OK
        assert Contact(**response.json())  # validation

    def test_edit_contact(self, client: TestClient, headers: dict):
        # Check for authorizations
        response = client.put("/contact", json=self.contact.dict())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Edit the contact informations
        response = client.put("/contact", json=self.contact.dict(), headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.contact.dict()

    def test_check_edited_contact(self, client: TestClient):
        # Check that the contact was really modified
        response = client.get("/contact")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.contact.dict()
