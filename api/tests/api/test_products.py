from api.schemas import PriceType, Product


class TestProduct:
    product = Product(
        name='Haché',
        categorie='Viande',
        description='A consommer avec modération.',
        price=4.5,
        price_type=PriceType.kilo
    )

    def test_get_products_empty(self, client):
        response = client.get("/products")
        assert response.status_code == 200
        assert response.json() == []

    def test_add_product(self, client, token):
        response = client.post("/products", json=self.product.dict())
        assert response.status_code == 401

        response = client.post("/products", json=self.product.dict(), headers=dict(Authorization=token))
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data.get('id'), int)
        self.product.id = data.get('id')
        assert Product(**response.json()) == self.product

    def test_get_products(self, client):
        response = client.get("/products")
        assert response.status_code == 200
        assert response.json() == [self.product.dict()]

    def test_get_images_empty(self, client):
        response = client.get(f"/products/{self.product.id}/images")
        assert response.status_code == 200
        assert response.json() == self.product.photos

        response = client.get("/products/9999/images")
        assert response.status_code == 404

    def test_update_product_visibility(self, client, token):
        response = client.put(f"/products/{self.product.id}/visibility", json=dict(visibility=True))
        assert response.status_code == 401

        headers = dict(Authorization=token)
        response = client.put(f"/products/{self.product.id}/visibility", json=dict(visibility=True), headers=headers)
        visible = self.product.dict()
        visible['visibility'] = True
        assert response.status_code == 200
        assert response.json() == visible

        response = client.put(f"/products/{self.product.id}/visibility", json=dict(visibility=False), headers=headers)
        assert response.status_code == 200
        assert response.json() == self.product.dict()
