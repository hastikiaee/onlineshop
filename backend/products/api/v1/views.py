from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin

from inventory.models import Category,Product,Color,Size,ProductVariant
from inventory.api.v1.serializers import ColorSerializer,SizeSerializer
from .serializers import CategoryMenuSerializer,ProductVariantSerializer
from .paginations import ProductPagination
from .filters import ProductFilter





class CategoryMenuListView(GenericAPIView,ListModelMixin):

    #retrevie category list for menue (only cat.name field)
    queryset=Category.objects.all()
    serializer_class=CategoryMenuSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

class ProductListView(GenericAPIView,ListModelMixin):
    
    #retrieve is_active products for all users
    queryset=Product.objects.filter(is_active=True)
    serializer_class=ProductVariantSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductFilter
    search_fields=['description','variants__color__name','name','variants__size__name','category__name']
    ordering_fields=['default_price','created_date']
    pagination_class=ProductPagination

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
class ProductColorListView(GenericAPIView,ListModelMixin):
     
    serializer_class=ColorSerializer

    def get_queryset(self):

        size_id= self.request.query_params.get("size_id")
        pk=self.kwargs.get("pk")

        queryset=   Color.objects.filter(variants__product=pk)

        if size_id:
            queryset = queryset.filter(variants__size=size_id)
        return queryset.distinct()

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
class ProductSizeListView(GenericAPIView,ListModelMixin):
     
    serializer_class=SizeSerializer

    def get_queryset(self):

        color_id = self.request.query_params.get("color_id")
        pk = self.kwargs.get("pk")

        queryset = Size.objects.filter(
            variants__product=pk
        )

        if color_id:
            queryset = queryset.filter(
                variants__color=color_id
            )

        return queryset.distinct()

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

class ProductDetailView(GenericAPIView,RetrieveModelMixin):
     
    queryset = Product.objects.filter(is_active=True).prefetch_related(
        Prefetch(
            "variants",
            queryset=ProductVariant.objects.select_related("color", "size")
        )
    )
    lookup_field='pk'
    serializer_class=ProductVariantSerializer
    def get(self,request,*args,**kwargs):
        return self.retrieve(request, *args, **kwargs)
