from django.test import TestCase
from django.urls import reverse
from inventory.models import Product,Category
from products.api.v1.views import ProductDetailView



# Create your tests here.
class TestUrls(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="test")

        self.product = Product.objects.create(
            name='test',
            default_price="1"
        )
        self.product.category.set([self.category])
        self.url=reverse("product_detail", kwargs={"pk": self.product.pk})


    def test_product_detail_response(self):
        response=self.client.get(self.url)
        self.assertEqual(response.status_code,200)

        