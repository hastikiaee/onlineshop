from django.contrib import admin
from carts.models import Cart,CartItem,ProductVariant

# Register your models here.

class CartItemAdmin(admin.TabularInline):

    model=CartItem
    autocomplete_fields=['variant']
    

class CartAdmin(admin.ModelAdmin):
    model=Cart
    list_display=["session","user"]
    inlines=[CartItemAdmin]

admin.site.register(Cart,CartAdmin)

class VariantAdmin(admin.ModelAdmin):
    model=ProductVariant
    list_display=['product','size','color']
    search_fields=['product','size','color']
admin.site.register(ProductVariant,VariantAdmin)
