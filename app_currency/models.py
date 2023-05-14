""" This module is used to define the models for the app_currency app. """""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CurrencyPackage(models.Model):
    """This model is used to store the currency packages that will be available for purchase."""

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    og_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    stripe_price = models.IntegerField(blank=True)
    in_app_currency = models.IntegerField()
    purchases = models.ManyToManyField(
        User,
        related_name=_("currency_package_purchases"),
        related_query_name=_("currency_package_purchase"),
        blank=True,
    )
    usage_count = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"

    def save(self, *args, **kwargs):
        """ This method is used to update the stripe_price
        field when the price field is updated. """ ""
        if self.price != self.og_price:
            self.og_price = self.price
            # Stripe price is in cents
            self.stripe_price = int(self.price * 100)
        super().save(*args, **kwargs)

