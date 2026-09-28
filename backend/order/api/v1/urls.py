from django.contrib import admin
from django.urls import path,include
from .views import OrderViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('order_items', OrderViewset,basename="order_items")

urlpatterns = [

   path('', include(router.urls))
]