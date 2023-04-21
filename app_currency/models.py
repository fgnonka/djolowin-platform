from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CurrencyPackage(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_app_currency = models.IntegerField()
    purchases = models.ManyToManyField(
        User, 
        related_name=_('currency_package_purchases'),
        related_query_name=_('currency_package_purchase'),
        blank=True
    )
    usage_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - ${self.price}"
    

