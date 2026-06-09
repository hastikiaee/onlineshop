from django.core.management.base import BaseCommand, CommandError
from ...models import Color,Size,Category,Product,ProductVariant

from faker import Faker
import random

SIZE_List=["large",'M','S',"xl",'xs']


class Command(BaseCommand):
    help = "creating fack color"

    def __init__(self, *args,**kwargs):
        super(Command,self).__init__(*args,**kwargs)
        self.fake=Faker()



    def handle(self, *args, **options):
        #create fake colors
        for _ in range(10):
            color_name=self.fake.color_name()
            Color.objects.get_or_create(name=color_name)
        #create sizes
        for size in SIZE_List:
            Size.objects.get_or_create(name=size)
        #create fake categories
        for _ in range(10):
            Category.objects.get_or_create(name=self.fake.words())
            
        #Create fake product
        categories=list(Category.objects.all())
        for _ in range(10):
            category = random.choice(categories)
            
            products,created=Product.objects.get_or_create(
                name=self.fake.word(),
                description=self.fake.sentence(),
                default_price=self.fake.random_int(min=100000, max=5000000),
            )
            if created:
                products.category.add(category)

            
        
        #create 10 variants for each product
        products=Product.objects.all()
        colors=list(Color.objects.all())
        sizes=list(Size.objects.all())
        for item in products:
            for _ in range(10):
            
                color=random.choice(colors)
                size=random.choice(sizes)
                ProductVariant.objects.get_or_create(
                    product=item,
                    stock=self.fake.random_int(min=0, max=10000),
                    color=color,
                    size=size

                )

   





        
        


