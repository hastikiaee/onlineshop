from django.contrib import admin
from .models import Product,Color,Size,ProductVariant,Category

# Register your models here.
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    autocomplete_fields = ['color', 'size']

class ProductAdmin(admin.ModelAdmin):
    model=Product
    list_display=('name','id')
    autocomplete_fields = ['category']
    inlines=[ProductVariantInline]

admin.site.register(Product,ProductAdmin)



class ColorAdmin(admin.ModelAdmin):
    model=Color
    list_display=("name","id")
    search_fields=("name",)

admin.site.register(Color,ColorAdmin)

class SizeAdmin(admin.ModelAdmin):
    model=Size
    list_display=("name",'id')
    search_fields=("name",)
admin.site.register(Size,SizeAdmin)

class CategoryAdmin(admin.ModelAdmin):
    model=Category
    list_display=("name",'id')
    search_fields=("name",)
admin.site.register(Category,CategoryAdmin)