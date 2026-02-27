from django.contrib import admin
from django.urls import path

from .views import CategoryMenuListView,ProductListView,ProductColorListView,ProductSizeListView,ProductDetailView

urlpatterns=[
    path("categories/",view=CategoryMenuListView.as_view(),name="category_menu_list"),
    path("products/",view=ProductListView.as_view(),name="product_list"),
    path("products/<int:pk>/colors/",view=ProductColorListView.as_view(),name="product_color_list"),
    path("products/<int:pk>/sizes/",view=ProductSizeListView.as_view(),name="product_size_list"),
    path("products/<int:pk>/",view=ProductDetailView.as_view(),name="product_detail"),
]