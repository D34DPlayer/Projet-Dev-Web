from fastapi import status
from fastapi.testclient import TestClient

from api.schemas import PriceType, Product


class TestProduct:
    product = Product(
        name="Haché",
        categorie="Viande",
        description="A consommer avec modération.",
        price=4.5,
        price_type=PriceType.kilo,
    )

    def test_add_product(self, client: TestClient, headers: dict):
        # Check for authorizations
        response = client.post("/products", json=self.product.dict())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Add a product
        response = client.post("/products", json=self.product.dict(), headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json().get("id"), int)  # The id must be given and should be an integer
        self.product.id = response.json().get("id")  # Assign it so we can use it later and use Pydantic validation
        assert response.json() == self.product

    def test_get_products(self, client: TestClient):
        # Check if the product we added in the previous test has been added.
        # We run the tests against a fresh database every time, so it should contain only our product.
        response = client.get("/products", params=dict(size=24))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['page'] == 1
        assert response.json()['size'] == 24
        assert response.json()['total'] == 1
        assert response.json()['items'] == [self.product]

        # Check the second page. We should get an empty list
        response = client.get("/products", params=dict(size=24, page=2))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['page'] == 2
        assert response.json()['size'] == 24
        assert response.json()['total'] == 1
        assert response.json()['items'] == []

        # Check an invalid page.
        response = client.get("/products", params=dict(page=0))
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Check a really big page.
        response = client.get("/products", params=dict(size=99999))
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_product_visibility(self, client: TestClient, headers: dict):
        # Check for authorizations
        response = client.put(f"/products/{self.product.id}/visibility", json=dict(visibility=True))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Update the visibility of a non-existant product.
        response = client.put("/products/666/visibility", json=dict(visibility=True), headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Update the visibility of our product.
        response = client.put(f"/products/{self.product.id}/visibility", json=dict(visibility=True), headers=headers)
        visible = self.product.dict()  # Copy the product
        visible["visibility"] = True  # and update it's visibility to true.
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == visible

        # Set the visibility back to false.
        response = client.put(f"/products/{self.product.id}/visibility", json=dict(visibility=False), headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.product.dict()

    def test_update_product_stock(self, client: TestClient, headers: dict):
        # Check for authorizations
        response = client.put(f"/products/{self.product.id}/stock", json=dict(stock=True))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Update the stock of a non-existant product.
        response = client.put("/products/666/stock", json=dict(stock=True), headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Update the stock of our product.
        response = client.put(f"/products/{self.product.id}/stock", json=dict(stock=False), headers=headers)
        out_of_stock = self.product.dict()  # Copy the product
        out_of_stock["stock"] = False  # and update it's stock to true.
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == out_of_stock

        # Set the stock back to true.
        response = client.put(f"/products/{self.product.id}/stock", json=dict(stock=True), headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.product.dict()

    def test_get_images_empty(self, client: TestClient):
        # Check the product's images before uploading. It should be empty.
        response = client.get(f"/products/{self.product.id}/images")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

        # It must return a 404 error when the product doesn't exists.
        response = client.get("/products/9999/images")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_upload_images(self, client: TestClient, headers: dict):
        files = [
            ["files", ("file1.png", "image_data", "image/png")],
            ["files", ("file2.png", "image_data", "image/png")],
        ]
        invalid_files = {"files": ("file3.png", "data", "text/html")}

        # Check for authorizations
        response = client.post(f"/products/{self.product.id}/images")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # It must return a 400 error when you send a file that isn't an image.
        # The api doesn't check the image's content but the mime-type instead.
        # It might lead to XSS attacks, but only trusted people can upload images.
        response = client.post(f"/products/{self.product.id}/images", files=invalid_files, headers=headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Check for a product that doesn't exists
        response = client.post("/products/666/images", files=files, headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Send two files: file1.png and file2.png
        # It should return the full path of both uploaded images in a list.
        response = client.post(f"/products/{self.product.id}/images", files=files, headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list) and len(response.json()) == 2
        assert response.json()[0].endswith("file1.png")
        assert response.json()[1] == f"/images/products/{self.product.id}/file2.png"

        # Send the files once more. It should conflict with the images already added and return a 409 error.
        response = client.post(f"/products/{self.product.id}/images", files=files, headers=headers)
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_get_images(self, client: TestClient):
        files = ["file1.png", f"/images/products/{self.product.id}/file2.png"]

        # Check that the images previously inserted were added.
        response = client.get(f"/products/{self.product.id}/images")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list) and len(response.json()) == 2
        assert response.json()[0].endswith(files[0])
        assert response.json()[1] == files[1]

    def test_delete_images(self, client: TestClient, headers: dict):
        files = ["file1.png", f"/images/products/{self.product.id}/file2.png"]

        # Check for authorizations
        response = client.delete(f"/products/{self.product.id}/images")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Check for a product that doesn't exists
        response = client.delete("/products/666/images", json=files, headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Delete an image that doesn't exist. It won't return any error, but won't remove anything.
        response = client.delete(f"/products/{self.product.id}/images", json=["file3.png"], headers=headers)
        assert response.status_code == status.HTTP_200_OK
        # Both files should still exists.
        assert isinstance(response.json(), list) and len(response.json()) == 2
        assert response.json()[0].endswith(files[0])
        assert response.json()[1] == files[1]

        # Delete both files.
        response = client.delete(f"/products/{self.product.id}/images", json=files, headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

        # Delete both files again.
        response = client.delete(f"/products/{self.product.id}/images", json=files, headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_edit_product(self, client: TestClient, headers: dict):
        product = self.product.dict()
        product["description"] = "A ne consommer que les mardis à 14h."

        # Check for authorizations
        response = client.put(f"/products/{self.product.id}", json=product)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Update a product that doesn't exist. It should return a 404 error.
        response = client.put("/products/666", json=product, headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Update the product's description.
        response = client.put(f"/products/{self.product.id}", json=product, headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == product

        # Update the new description for the following tests.
        self.product.description = response.json().get("description")

    def test_delete_product(self, client: TestClient, headers: dict):
        # Check for authorizations
        response = client.delete(f"/products/{self.product.id}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Check for a product that doesn't exists
        response = client.delete("/products/666", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Delete the product.
        response = client.delete(f"/products/{self.product.id}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.product

        # Check that the product does not exists anymore.
        response = client.get("/products")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['total'] == 0
        assert response.json()['items'] == []
