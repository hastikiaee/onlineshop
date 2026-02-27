from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid

def variant_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'products/{instance.product.id}/{filename}'

class Category(models.Model):
    
    image=models.ImageField(_("image"),upload_to='category/')
    name=models.CharField(_("name"),max_length=50) 
    def __str__(self):
        return self.name

class Product(models.Model):
    

    name=models.CharField(_("name"),max_length=50)
    description = models.TextField(_("description"),blank=True)
    category = models.ManyToManyField(Category,verbose_name=_('category'),related_name='product') 
    default_price = models.PositiveBigIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    def __str__(self):
        return self.name


    
class Color(models.Model):

    name=models.CharField(unique=True,verbose_name=_("name"),max_length=50,null=True,blank=True)
    def __str__(self):
        return self.name

class Size(models.Model):

    name=models.CharField(unique=True,verbose_name=_("name"),max_length=50)
    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    
    image=models.ImageField(_("image"),null=True,blank=True,upload_to= variant_image_upload_path)
    product=models.ForeignKey(Product,verbose_name=_("product"),on_delete=models.CASCADE,related_name="variants")
    color=models.ForeignKey(Color,verbose_name=_("color"),on_delete=models.PROTECT,related_name="variants")
    size=models.ForeignKey(Size,verbose_name=_("size"),on_delete=models.PROTECT,related_name="variants")
    price=models.PositiveBigIntegerField(_("price"),null=True,blank=True)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name}-{self.size}-{self.color}'