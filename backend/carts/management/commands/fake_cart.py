from django.core.management.base import BaseCommand, CommandError
from ...models import CartItem,Cart
from acounts.models import CustomUser
from inventory.models import ProductVariant
from faker import Faker
import random




class Command(BaseCommand):
    help = "creating fake cart and cart items"

    def __init__(self, *args,**kwargs):
        super(Command,self).__init__(*args,**kwargs)
        self.fake=Faker()



    def handle(self, *args, **options):
        users=CustomUser.objects.all()
        for user in users:
            cart=Cart.objects.create(user=user)
            random_int=random.randrange(0,10)
            variants=list(ProductVariant.objects.all())
            for _ in range(random_int):
                variant=random.choice(variants)
                quantity=random.randrange(0,5)
                CartItem.objects.create(variant=variant,cart=cart,quantity=quantity)

            


   





        
        


