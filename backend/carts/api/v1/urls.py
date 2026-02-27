from django.contrib import admin
from django.urls import path,include
from .view import CartItemViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('cart_items', CartItemViewSet,basename="cart_items")

urlpatterns = [
   #path("cart_items/",view=CartItemViewSet.as_view({'post':'add','get':'get_cart','patch':'increase'}),name='cart_items'),
   #path("cart_items/<int:pk>/",view=CartItemViewSet.as_view({'delete':'destroy'}),name='cart_items'),
   #path("cart_items/decrease/",view=CartItemViewSet.as_view({'patch':'decrease'}),name="cart_items_decrase")
   #path('cart/',CartItemViewSet.as_view({'get': 'get_card'}),name='get-card'),
   path('', include(router.urls))
]