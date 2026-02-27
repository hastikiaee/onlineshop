from .serializer import CartItemSerializer,CartSerializer

from rest_framework import viewsets
from rest_framework.decorators import action
from ...models import Cart,CartItem
from rest_framework.response import Response
from rest_framework import status
from inventory.models import ProductVariant
from django.shortcuts import get_object_or_404
from .services import get_or_create_cart
from .permissions import IsOwner

class CartItemViewSet(viewsets.ViewSet):

    serializer_class=CartItemSerializer
    queryset=Cart.objects.all()
    permission_classes=[IsOwner]
    


    #add a variant with quantity to cart
    @action(detail=False,methods=['post'])
    def add(self,request):
        serializer=self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    #get to user his/her cart with all of its items and total price and sub total price
    @action(detail=False,methods=['get'],url_name='get',url_path='get')
    def get_cart(self,request):
        user=request.user
        if user:
            queryset=self.queryset.filter(user=user)
        else:
            session=request.session.session_key
            if not session:
                request.session.create()
                session = request.session.session_key
            queryset=self.queryset.filter(session=session)
                
        serializer=CartSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    #add 1 to a cartitem containing an special variant
    @action(detail=False,methods=['patch'])
    def increase(self,request):
        variant=request.data.get('variant')
        data={"variant":variant,"quantity":1}
        serializer=self.serializer_class(data=data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    #delete 1 from a cart item containing an special variant 
    #if quantyty of the cart item reach to zero delete the cart item
    @action(detail=False,methods=["patch"])
    def decrease(self,request):
        cart=get_or_create_cart(request)
        variant=request.data.get('variant')
        cart_item=CartItem.objects.filter(cart=cart,variant=variant).first()
        if cart_item:
            cart_item.quantity+=-1
            if cart_item.quantity==0:
                cart_item.delete()
                return Response({"detail":'محصول مورد نظر حدف شد'})
            else:
                cart_item.save()
                return Response({"detail":"محصول مورد نظر کم شد"})
                
        else:
            return Response({'detail':"این محصول در سبد خرید موجود نیست"}) 
    #delete a cart item with its id
    def destroy(self,request,pk=None):

        cart_item=get_object_or_404(CartItem,pk=pk)
        self.check_object_permissions(request, cart_item)
      
        cart_item.delete()
        return Response({"detail":"ایتم مورد نظر حدف شد"},status=status.HTTP_204_NO_CONTENT)


        
