from django_filters import rest_framework as filters
from inventory.models import Product

class NumberInField (filters.BaseInFilter,filters.NumberFilter):
    pass
class ProductFilter(filters.FilterSet):
 
    min_price=filters.NumberFilter(field_name='default_price',lookup_expr='gte')
    max_price=filters.NumberFilter(field_name='default_price',lookup_expr='lte')
    category=NumberInField(field_name='category',lookup_expr='in')

    class Meta:
        model=Product
        fields=['default_price','category','variants__size','variants__color']   