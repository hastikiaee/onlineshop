from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductVariantSerializer,ProductSerializer,ColorSerializer,SizeSerializer,CategorySerializer,VariantSerializer
from django.shortcuts import get_object_or_404
from ...models import Product,Color,Size,ProductVariant,Category
from django.db.models import ProtectedError

@api_view(["GET","PUT","DELETE"])
#@permission_classes([IsAdminUser])
def product_detail_view(request,pk):
    product=get_object_or_404(Product,pk=pk)
    #show product detail and its variants
    if request.method=='GET':
        product_data=ProductVariantSerializer(product).data
        return Response(product_data)
    #edit product only
    if request.method=="PUT":
        serializer=ProductSerializer(product,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    #delete product with all its variants
    if request.method=="DELETE":
        product.delete()
        return Response({"detail":"product successfully deleted"},status=status.HTTP_204_NO_CONTENT)

@api_view(["GET","POST"])
#@permission_classes([IsAdminUser])
def product_view(request):
    
    #add product whith at least one variant
    if request.method=='POST':
        serializer=ProductVariantSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
       
    #show all products to admin
    if request.method=='GET':
        products=Product.objects.all()
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)

#color
@api_view(["GET","POST"])
@permission_classes([IsAdminUser])
def color_view(request):
    #add color and view list of colors
    if request.method=='POST':
        serializer=ColorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    if request.method=="GET":
        colors=Color.objects.all()
        serializer=ColorSerializer(colors,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["DELETE","PUT"])
@permission_classes([IsAdminUser])
def color_detail_view(request, pk):

    #update or delete color
    color=get_object_or_404(Color,pk=pk)
    
    if request.method=="PUT":
       
        serializer=ColorSerializer(color,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
    
    if request.method=="DELETE":
        try:
            color.delete()
            return Response({"detail":"color successfully deleted"},status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response(
                    {"error": "این رنگ در محصولات استفاده شده و قابل حذف نیست."},
                     status=status.HTTP_400_BAD_REQUEST
                    )
       
        
#size

@api_view(['POST',"GET"])
@permission_classes([IsAdminUser])
def size_view(request):

    #add size and view list of sizes
    if request.method=='POST':
        serializer=SizeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
    if request.method=="GET":    
        sizes=Size.objects.all()
        serializer=SizeSerializer(sizes,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
@api_view(["DELETE","PUT"])
@permission_classes([IsAdminUser])
def size_detail_view(request, pk):
    #size delete or update
    size=get_object_or_404(Size,pk=pk)
    if request.method=="PUT":
       
        serializer=SizeSerializer(size,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
    
    if request.method=="DELETE":
        try:
            size.delete()
            return Response({"detail":"color successfully deleted"},status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response(
                    {"error": "این رنگ در محصولات استفاده شده و قابل حذف نیست."},
                     status=status.HTTP_400_BAD_REQUEST
                    )
       


#variant update and delete
@api_view(["DELETE","PUT"])
@permission_classes([IsAdminUser])
def variant_view(request,pk):
    #variant update or delete
    variant=get_object_or_404(ProductVariant,pk=pk)
    if request.method=="PUT":
        serializer=VariantSerializer(variant,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
    if request.method=="DELETE":
        variant.delete()
        return Response({"detail":"variant successfully deleted"},status=status.HTTP_204_NO_CONTENT)

#category
@api_view(["POST",'GET'])
#@permission_classes([IsAdminUser])
def category_view(request):

    #add category and view list of categorys
    if request.method=='POST':
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
    if request.method=="GET":    
        categories=Category.objects.all()
        serializer=CategorySerializer(categories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
@api_view(["DELETE","PUT"])
@permission_classes([IsAdminUser])
def category_detail_view(request, pk):
    #category delete or update
    category=get_object_or_404(Color,pk=pk)
    if request.method=="PUT":
       
        serializer=CategorySerializer(category,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
    
    if request.method=="DELETE":
        try:
            category.delete()
            return Response({"detail":"color successfully deleted"},status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response(
                    {"error": "این دسته بندی در محصولات استفاده شده و قابل حذف نیست."},
                     status=status.HTTP_400_BAD_REQUEST
                    )

      