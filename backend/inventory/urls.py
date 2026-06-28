from django.contrib import admin
from django.urls import path,include

from .views import Inventory,InventoryDetail


urlpatterns = [
    
    path("api/v1/",include('inventory.api.v1.urls')),
    path("inventory/",view=Inventory.as_view(),name='inventory'),
    path("inventory/detail/<int:pk>/",view=InventoryDetail.as_view(),name='inventory-detail')
    
]