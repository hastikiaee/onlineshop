from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.
class Inventory(TemplateView):
    template_name='inventory.html'

class InventoryDetail(TemplateView):
    template_name='inventory_detail.html'