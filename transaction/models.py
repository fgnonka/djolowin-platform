from django.conf import settings
from django.db import models

# from playercard.models import PlayerCard
# from bundle.models import Bundle

User = settings.AUTH_USER_MODEL

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('card_purchase', 'Card Purchase'),
        ('bundle_purchase', 'Bundle Purchase'),
        ('currency_purchase', 'Currency Purchase')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    card = models.ForeignKey('playercard.PlayerCard', on_delete=models.SET_NULL, null=True, blank=True)
    bundle = models.ForeignKey('bundle.Bundle', on_delete=models.SET_NULL, null=True, blank=True)
    currency_package = models.ForeignKey('app_currency.CurrencyPackage', on_delete=models.SET_NULL, null=True, blank=True)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.timestamp.__format__('%Y-%m-%d %H:%M:%S')}"
