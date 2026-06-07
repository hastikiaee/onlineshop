from django.db import models
from django.utils.translation import gettext_lazy as _
from acounts.models import CustomUser
from inventory.models import ProductVariant



# Create your models here.

class Cart(models.Model):
  
    user=models.OneToOneField(CustomUser,verbose_name=_("user"),on_delete=models.CASCADE,related_name="cart",null=True,blank=True)
    total_price=models.PositiveBigIntegerField(_("total_price"))
    session=models.CharField(_("session"),blank=True,null=True)

    def __str__(self):
        if self.user:
            return self.user.email
        return self.session or "Guest Cart"
    
    @property
    def total_price(self):
        return sum(item.subtotal_price for item in self.items.all())


class CartItem(models.Model):

    variant=models.ForeignKey(ProductVariant,verbose_name=_("variant"),on_delete=models.PROTECT,related_name='items')
    quantity=models.PositiveIntegerField(_("quantity"),default=1)
    cart=models.ForeignKey(Cart,verbose_name=_("cart"),on_delete=models.CASCADE,related_name="items")

    def __str__(self):
        return f'{self.variant.product}-{self.variant.color}-{self.variant.size}'
    
    @property
    def subtotal_price(self):
        return self.variant.price*self.quantity
