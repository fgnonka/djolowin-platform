from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.utils import timezone
from playercard.models import PlayerCard

from account.models import CustomUser
from wallet.models import UserWallet


class Auction(models.Model):
    card = models.ForeignKey(PlayerCard, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    starting_price = models.PositiveIntegerField(validators=[MinValueValidator(2000)])
    current_bid = models.PositiveIntegerField(default=0)
    highest_bidder = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        related_name="highest_bidder",
        on_delete=models.SET_NULL,
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    watchers = models.ManyToManyField(CustomUser, related_name="watched_auctions")
    auction_ended = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["-start_time"]
        constraints = [
            UniqueConstraint(fields=["card", "owner"], name="unique_auction")
        ]
        
    @property
    def already_active(self):
        existing_active_auction = Auction.objects.filter(
            Q(card=self.card) & Q(owner=self.owner) & Q(end_time__gte=timezone.now())
        )
        if existing_active_auction:
            return True
        else:
            return False

    @property
    def has_ended(self):
        now = timezone.now()
        return self.end_time <= now

    @property
    def is_ending_soon(self):
        now = timezone.now()
        return self.end_time - now < timezone.timedelta(hours=1)
    
    
    def is_active(self):
        now = timezone.now()
        return self.start_time <= now and self.end_time >= now

    def __str__(self):
        return f"{self.card} - Auction by {self.owner}"

    def accept_bid(self, user, amount):
        wallet = UserWallet.objects.get(user=user)
        if self.is_active():
            if (
                amount > self.starting_price
                and amount > self.current_bid
                and wallet.available_balance >= amount
            ):
                wallet.reserved_balance += amount
                self.current_bid = amount
                self.highest_bidder = user
                wallet.save()
                return True
        return False
    

    def get_highest_bid(self):
        return Bid.objects.filter(auction=self).order_by("-amount").first()


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} - Bid on {self.auction}"

    def save(self, *args, **kwargs):
        if self.auction.is_active():
            super().save(*args, **kwargs)
        else:
            raise Exception("Auction is not active.")
