from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


# Generate a unique upload path for each variant image
# Path format: products/<product_id>/<random_uuid>.<ext>
def variant_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]  # get file extension
    filename = f"{uuid.uuid4()}.{ext}"  # generate unique filename
    return f'products/{instance.product.id}/{filename}'


class Category(models.Model):
    # Image representing the category
    image = models.ImageField(_("image"), upload_to='category/')

    # Category name (must be unique)
    name = models.CharField(_("name"), max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    # Product name
    name = models.CharField(_("name"), max_length=50)

    # Optional product description
    description = models.TextField(_("description"), blank=True)

    # Product can belong to multiple categories
    category = models.ManyToManyField(
        Category,
        verbose_name=_('category'),
        related_name='product'
    )

    # Default/base price of the product
    default_price = models.PositiveBigIntegerField()

    # Indicates whether the product is active and visible
    is_active = models.BooleanField(default=True)

    # Timestamp when the product was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Timestamp when the product was last updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    # Color name (unique but optional)
    name = models.CharField(
        unique=True,
        verbose_name=_("name"),
        max_length=50,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Size(models.Model):
    # Size label (e.g., S, M, L, XL)
    name = models.CharField(
        unique=True,
        verbose_name=_("name"),
        max_length=50
    )

    def __str__(self):
        return self.name


class ProductVariant(models.Model):

    # Optional image for this specific variant
    image = models.ImageField(
        _("image"),
        null=True,
        blank=True,
        upload_to=variant_image_upload_path
    )

    # Parent product
    product = models.ForeignKey(
        Product,
        verbose_name=_("product"),
        on_delete=models.CASCADE,
        related_name="variants"
    )

    # Variant color
    color = models.ForeignKey(
        Color,
        verbose_name=_("color"),
        on_delete=models.PROTECT,
        related_name="variants"
    )

    # Variant size
    size = models.ForeignKey(
        Size,
        verbose_name=_("size"),
        on_delete=models.PROTECT,
        related_name="variants"
    )

    # Optional specific price for this variant
    # If null, product.default_price can be used
    price = models.PositiveBigIntegerField(
        _("price"),
        null=True,
        blank=True
    )

    # Available inventory count
    stock = models.PositiveIntegerField(default=0)

    # Optional Stock Keeping Unit identifier
    sku = models.CharField(max_length=50, blank=True, null=True)

    # Indicates if this variant is available for purchase
    is_active = models.BooleanField(default=True)

    # Creation timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    # Last update timestamp
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name}-{self.size}-{self.color}'
