from django.db import models

from apps.common.models import TimeStampedModel
from apps.orders.models import Order


class PaymentTransaction(TimeStampedModel):
    STATUS_CHOICES = (
        ("created", "Created"),
        ("successful", "Successful"),
        ("failed", "Failed"),
    )
    PROVIDER_CHOICES = (
        ("fake", "Fake"),
        ("click", "Click"),
        ("payme", "Payme"),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default="fake")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    external_reference = models.CharField(max_length=255, blank=True)
