
from rest_framework import viewsets
from rest_framework.decorators import action
from ...models import Order, OrderItem
from rest_framework.response import Response
from rest_framework import status
from inventory.models import ProductVariant
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializer import OrderSerializer, OrderItemSerializer
from carts.api.v1.permissions import IsOwner
from carts.models import Cart, CartItem
from django.db import transaction


# put / patch / delete / retrieve / get / add
class OrderViewset(viewsets.ModelViewSet):

    serializer_class = OrderSerializer

    permission_classes = [IsOwner]

    # For get or retrieve
    # This method makes sure that each user can only access their own orders.
    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        )

    # Make an order with all of the items in the customer's cart
    @action(detail=False, methods=['post'])
    def add(self, request):

        user = request.user

        # Get the user's cart and prefetch its items and their variants.
        # prefetch_related is used because "items" is a reverse relation.
        cart = get_object_or_404(
            Cart.objects.prefetch_related('items__variant'),
            user=user
        )

        # Get all CartItems from the user's cart.
        # list() evaluates the QuerySet and stores the items in memory.
        cartitems = list(cart.items.all())

        # Check if the cart is empty.
        if not cartitems:
            return Response(
                {"detail": "سبد خرید خالی است."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate the total price of the cart.
        total_price = cart.total_price

        # Make sure creating the order and its items
        # are treated as one database transaction.
        with transaction.atomic():

            # Create the main Order.
            order = Order.objects.create(
                total_price=total_price,
                user=user
            )

            # Create an OrderItem for every CartItem.
            for item in cartitems:

                # Calculate the subtotal price of the current cart item.
                subtotalprice = item.subtotal_price

                # Create the OrderItem and connect it to the Order.
                OrderItem.objects.create(
                    variant=item.variant,
                    unit_price=subtotalprice,
                    quantity=item.quantity,
                    order=order
                )

        # Get all OrderItems belonging to the newly created Order
        # and serialize them for the response.
        orderitems = OrderItemSerializer(
            OrderItem.objects.filter(order=order),
            many=True
        ).data

        # Return the created order information.
        return Response(
            {
                "order_id": order.id,
                "total_price": order.total_price,
                "items": orderitems
            },
            status=status.HTTP_201_CREATED
        )

