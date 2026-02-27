from django.test import TestCase

from inventory.api.v1.views import Product,Category

# Create your tests here.
class TestUrls(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="test")

        self.product = Product.objects.create(
            name='test',
            default_price="1"
        )
        self.product.category.set([self.category])

    def test_product_model_create(self):
        id=self.product.id
        self.assertEqual(self.product.name,"test")
        self.assertTrue(Product.objects.get(id=id))