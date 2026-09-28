from django.core.management.base import BaseCommand, CommandError
from ...models import Order,OrderItem
from acounts.models import CustomUser
from carts.models import CartItem,Cart
from django.shortcuts import get_object_or_404
from faker import Faker
import random




class Command(BaseCommand):
    help = "creating fake order and order items"




    def handle(self, *args, **options):
        users=CustomUser.objects.all()
        for user in users:
            cart = get_object_or_404(
            Cart.objects.prefetch_related('items__variant'),
            user=user
            )
            total_price=random.randint(0,10)
            order=Order.objects.create(user=user,total_price=total_price)
            print(cart.items.all())
            for item in cart.items.all():
                variant=item.variant
                quantity=item.quantity
                OrderItem.objects.create(order=order,variant=variant,quantity=quantity,
                                         unit_price=random.randint(0,5))
            


   





        
        


