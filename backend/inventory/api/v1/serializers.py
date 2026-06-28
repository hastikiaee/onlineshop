from rest_framework import serializers
from ...models import Product,ProductVariant,Color,Size,Category


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model=Color
        fields="__all__"

class SizeSerializer(serializers.ModelSerializer):

    class Meta:
        model=Size
        fields="__all__"

#variant serializer
class VariantSerializer(serializers.ModelSerializer):

    color_name = serializers.CharField(
        source='color.name',
        read_only=True
    )

    size_name = serializers.CharField(
        source='size.name',
        read_only=True
    )

    class Meta:
        model=ProductVariant
        exclude=["product"]
        read_only_fields=["created_at","updated_at"]

#serializer for both product and its variants
class ProductVariantSerializer(serializers.ModelSerializer):
    
    variants=VariantSerializer(many=True)
    
    class Meta:
        model=Product
        fields="__all__"
        read_only_fields=["created_at","updated_at"]
        

    def create(self,validated_data):
        
        variants=validated_data.pop("variants")
        category_queryset=validated_data.pop("category")
        product=Product.objects.create(**validated_data)
        product.category.set(category_queryset)

        for variant in variants:
            ProductVariant.objects.create(product=product,**variant)
        return product

#serializer for product model only
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        fields="__all__"



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model=Category
        fields=['id','name','image']