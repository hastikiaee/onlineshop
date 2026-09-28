from django.core.management.base import BaseCommand, CommandError
from ...models import UserProfile,CustomUser
from faker import Faker
import random




class Command(BaseCommand):
    help = "creating fake user"

    def __init__(self, *args,**kwargs):
        super(Command,self).__init__(*args,**kwargs)
        self.fake=Faker()



    def handle(self, *args, **options):
        #create fake colors
        for _ in range(10):
            email=self.fake.email()
            password=self.fake.password()
            user=CustomUser.objects.create_user(email=email,password=password)
           
            


   





        
        


