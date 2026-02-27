from django.test import TestCase
from django.urls import resolve,reverse
from products.api.v1.views import CategoryMenuListView

# Create your tests here.
class TestUrls(TestCase):

    def test_category_menu_url_resolve(self):
        urls=reverse("category_menu_list")
        self.assertEqual(resolve(urls).func.view_class,CategoryMenuListView)