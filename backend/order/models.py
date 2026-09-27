from django.db import models
from django.utils.translation import gettext_lazy as _
from acounts.models import CustomUser
from inventory.models import ProductVariant



class Order(models.Model):

    class Status(models.TextChoices):
        PENDING_PAYMENT = "pending_payment", "در انتظار پرداخت"
        PAID = "paid", "پرداخت شده"
        CANCELLED = "cancelled", "لغو شده"
        REFUND_PENDING = "refund_pending", "در انتظار استرداد"
        REFUNDED = "refunded", "مبلغ مسترد شد"

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "در انتظار پرداخت"
        PAID = "paid", "پرداخت شده"
        REFUND_PENDING = "refund_pending", "در انتظار استرداد"
        REFUNDED = "refunded", "مسترد شده"

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    total_price = models.PositiveBigIntegerField()

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING_PAYMENT
    )

    authority = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    ref_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    refund_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)



class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(default=1)

    unit_price = models.PositiveBigIntegerField()

    @property
    def subtotal(self):
        return self.unit_price * self.quantity