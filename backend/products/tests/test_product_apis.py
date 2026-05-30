import pytest
from rest_framework.test import APIClient
from inventory.models import Product,Category
from django.urls import reverse


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def category(db):
    return Category.objects.create(name="test")

@pytest.fixture
def product(db, category):
    product= Product.objects.create(
        name="test",
        default_price=1,
    )
    product.category.add(category)
    return product

class TestProductDetailApi():

    @pytest.mark.django_db
    def test_product_detail_status_code_200(self,product,api_client):
        url=reverse("product_detail",kwargs={"pk":product.id})
        response=api_client.get(url)
        assert response.status_code == 200

