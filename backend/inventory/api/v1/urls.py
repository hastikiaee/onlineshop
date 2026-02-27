from django.contrib import admin
from django.urls import path
from .views import (product_detail_view,product_view,color_view,
                    size_view,color_detail_view,size_detail_view,variant_view,category_view,category_detail_view)




urlpatterns = [
    path('products/<int:pk>/',view=product_detail_view,name='product_detail'),
    path('products/',view=product_view,name='product_detail'),
    path("colors/",view=color_view,name="color_list"),
    path("sizes/",view=size_view,name="size_list"),
    path("categories/",view=category_view,name="category_list"),
    path("colors/<int:pk>/",view=color_detail_view,name="color_detail"),
    path("sizes/<int:pk>/",view=size_detail_view,name="size_detail"),
    path("categories/<int:pk>/",view=category_detail_view,name="category_detail"),
    path('products/variants/<int:pk>/',view=variant_view,name='variant')

]