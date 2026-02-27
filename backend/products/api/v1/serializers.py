from rest_framework import serializers
from inventory.models import Category,Product,ProductVariant


class CategoryMenuSerializer(serializers.ModelSerializer):

    class Meta:
        model=Category
        fields=["id",'name']



#variant serializer
class VariantSerializer(serializers.ModelSerializer):
    color=serializers.CharField(source='color.name')
    size=serializers.CharField(source='size.name')
    stock=serializers.SerializerMethodField()
    is_available=serializers.SerializerMethodField()
    class Meta:
        model=ProductVariant
        fields=['id','image','color','size','price','sku','is_active','created_at','stock','is_available']

    def get_stock(self,obj):
        if 0<=obj.stock<6:
            return obj.stock
        else:
            return None
    
    def get_is_available(self,obj):
        if obj.stock==0:
            return False
        elif obj.stock>0:
            return True


        

#serializer for both product and its variants
class ProductVariantSerializer(serializers.ModelSerializer):
    
    
    variants=VariantSerializer(many=True)
    class Meta:
        model=Product
        fields=['id',"name",'category','description','default_price','created_at','variants','is_active']
        
        

    def create(self,validated_data):
        
        variants=validated_data.pop("variants")
        category_queryset=validated_data.pop("category")
        product=Product.objects.create(**validated_data)
        product.category.set(category_queryset)

        for variant in variants:
            ProductVariant.objects.create(product=product,**variant)
        return product
    def to_representation(self, instance):
        request=self.context.get('request')
        rep= super().to_representation(instance)
        rep['category']=CategoryMenuSerializer(instance.category,context={request:request},many=True).data
        pk =request.parser_context.get("kwargs").get("pk")
        if not pk:
            rep.pop("description")
            rep.pop("variants")
        
        return rep
