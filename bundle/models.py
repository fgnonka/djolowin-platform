from django.db import models
from django.utils import timezone
from django.urls import reverse
from playercard.models import PlayerCard, CardRarity


class Bundle(models.Model):
    name = models.CharField(max_length=100)
    rarity = models.ForeignKey(CardRarity, on_delete=models.CASCADE)
    cards = models.ManyToManyField(PlayerCard, through="BundleCard", limit_choices_to={'owner': None})
    cover_image = models.ImageField(upload_to='bundle_covers/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_sold = models.DateTimeField(null=True, blank=True)
    sold_to = models.ForeignKey('account.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("bundle:bundle-detail", kwargs={"pk": self.pk})

    def mark_as_sold(self, buyer):
        self.sold_to = buyer
        self.is_available = False
        self.is_sold = True
        self.date_sold = timezone.now()
        self.save()
    
    @property
    def get_cards_in_bundle(self):
        return self.cards.all()

class BundleCard(models.Model):
    card_bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE)
    player_card = models.ForeignKey(PlayerCard, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.player_card} in {self.card_bundle}"

    class Meta:
        unique_together = ["card_bundle", "player_card"]