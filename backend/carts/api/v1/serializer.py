from ...models import Cart,CartItem
from rest_framework import serializers
from inventory.models import ProductVariant
from django.shortcuts import get_object_or_404
from .services import get_or_create_cart


class VariantSerializer(serializers.ModelSerializer):
    
    color=serializers.StringRelatedField()
    size=serializers.StringRelatedField()
    #for showing detail of each items
    class Meta:
        model=ProductVariant
        fields=['id','image','color','size','price','sku','is_active','created_at']
        read_only_fields=['id','image','color','size','price','sku','is_active','created_at']

class CartItemSerializer(serializers.ModelSerializer):
    
    #create or get cart and cart items with the two fieald quantity and variant 
    subtotal_price=serializers.IntegerField(read_only=True)
    

    class Meta:
        model = CartItem
        fields = ['id','quantity', 'variant','subtotal_price']
        read_only_fields = ['id','price','subtotal_price']

    def create(self, validated_data):
        
        request=self.context.get('request')
        cart=get_or_create_cart(request)
     
        variant=validated_data["variant"]
        quantity=validated_data["quantity"]
        #get or create cart_item
        cart_item,created=CartItem.objects.get_or_create(variant=variant,cart=cart,defaults={'quantity':quantity})
        
        #if cart item was already existed then just upadte quantity
        if not created :
            cart_item.quantity+=quantity
            cart_item.save()
        return cart_item
    
    def validate_quantity(self,value):

        request=self.context.get('request')

        user=request.user if request.user.is_authenticated else None
        session_key=request.session.session_key
        if not session_key:
            request.session.create()
        session = request.session.session_key

        cart_item_variant=self.initial_data.get('variant')
        variant=get_object_or_404(ProductVariant,id=cart_item_variant)
        if user:
            cart_item=CartItem.objects.filter(cart__user=user,variant=variant).first()
        elif session:
            cart_item=CartItem.objects.filter(cart__session=session,variant=variant).first()   
        current_quantity = cart_item.quantity if cart_item else 0
       
        if value+current_quantity > variant.stock:
                            raise serializers.ValidationError(
                    f"موجودی محصول کمتر از تعداد درخواستی شماست. موجودی فعلی: {variant.stock - current_quantity}"
                )
    
        return value
    def to_representation(self, instance):
        request=self.context.get('request')
        rep= super().to_representation(instance)
        rep['variant'] = VariantSerializer(instance.variant,read_only=True,context={'request':request}).data
        return rep
        

class CartSerializer(serializers.ModelSerializer):
    #showing cart with its items
    total_price=serializers.IntegerField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model=Cart
        fields=['id','total_price','items']
        read_only_fields=['id','total_price','items']