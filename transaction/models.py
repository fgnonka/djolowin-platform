from django.conf import settings
from django.db import models

# from playercard.models import PlayerCard
# from bundle.models import Bundle

User = settings.AUTH_USER_MODEL


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ("card_purchase", "Card Purchase"),
        ("bundle_purchase", "Bundle Purchase"),
    )

    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="buyer", null=True, blank=True
    )
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seller", null=True, blank=True
    )
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    card = models.ForeignKey(
        "playercard.PlayerCard", on_delete=models.SET_NULL, null=True, blank=True
    )
    bundle = models.ForeignKey(
        "bundle.Bundle", on_delete=models.SET_NULL, null=True, blank=True
    )
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.transaction_type == "card_purchase":
            return f"{self.buyer.username} - {self.transaction_type} - {self.card}"
        else:
            return f"{self.buyer.username} - {self.transaction_type} - {self.bundle}"

    def get_absolute_url(self):
        if self.transaction_type == "card_purchase":
            return self.card.get_absolute_url()
        else:
            return self.bundle.get_absolute_url()

class InAppCurrencyTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency_package = models.ForeignKey(
        "app_currency.CurrencyPackage", on_delete=models.SET_NULL, null=True, blank=True
    )
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)
    currency_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.currency_package.name} - {self.timestamp.__format__('%Y-%m-%d %H:%M:%S')}"


class AuctionTransaction(models.Model):
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="auction_seller"
    )
    winner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="auction_winner",
        null=True,
        blank=True,
    )
    auction = models.ForeignKey("auction.Auction", on_delete=models.CASCADE)
    start_price = models.PositiveIntegerField()
    winning_bid = models.PositiveIntegerField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    number_of_bids = models.PositiveIntegerField(default=0)
    number_of_watchers = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Auction by {self.seller.username} - {self.auction.card} - {self.start_time.__format__('%Y-%m-%d %H:%M:%S')} - {self.end_time.__format__('%Y-%m-%d %H:%M:%S')}"
