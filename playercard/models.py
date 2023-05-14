from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from base.models import Team
from django.core.validators import MinValueValidator


User = settings.AUTH_USER_MODEL


class CardRarity(models.Model):
    name = models.CharField(max_length=255, unique=True)

    @staticmethod
    def get_all_rarities():
        return CardRarity.objects.all()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Card Rarity"
        verbose_name_plural = "Card Rarities"


class PlayerCard(models.Model):
    """The base playercard object"""

    
    for_sale = models.BooleanField(default=True)
    edition = models.IntegerField(default=2024)
    is_public = models.BooleanField(
        _("Is public"),
        default=True,
        db_index=True,
        help_text=_("Show this playercard in search results and portfolios."),
    )
    owner = models.ForeignKey(
        "account.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="playercards",
    )
    player = models.ForeignKey(
        "base.Player",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="playercards",
    )
    rarity = models.ForeignKey(
        CardRarity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cards",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(2000)])
    image = models.ImageField(upload_to="uploads/playercards", null=True, blank=True)
    index = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    number_likes = models.PositiveIntegerField(_("Likes"), default=0)
    # portfolio = models.OneToOneField(Portfolio, on_delete=models.SET_DEFAULT, default=)
    date_created = models.DateTimeField(
        _("Date created"), auto_now_add=True, db_index=True
    )
    # This field is used by Haystack to reindex search
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)
    is_locked = models.BooleanField(default=False)
    class Meta:
        ordering = ["player"]
        verbose_name = _("Playercard")
        verbose_name_plural = _("Playercards")
        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["player"]),
            models.Index(fields=["rarity"]),
        ]

    def __str__(self):
        return f"{self.player} --- {self.rarity} --- {self.index}"

    def get_absolute_url(self):
        return reverse("playercard:playercard-detail", kwargs={"pk": self.pk})

    @property
    def teams(self):
        return [(t.id, t.name) for t in Team.objects.all()]

    @property
    def rarities(self):
        return [(r.id, r.name) for r in CardRarity.objects.all()]

    RARITIES = rarities

    @property
    def get_total_card_index(self):
        allcards = PlayerCard.objects.filter(
            Q(rarity=self.rarity) & Q(player=self.player) & ~Q(index=0)
        )
        return allcards.count()

    @staticmethod
    def get_all_cards():
        return PlayerCard.objects.all()

    def get_all_cards_by_player(self):
        return PlayerCard.objects.filter(player=self.player)

    def get_all_cards_by_owner(self):
        return PlayerCard.objects.filter(owner=self.owner)

    def get_number_of_cards(self):
        number_of_cards = PlayerCard.objects.filter(player=self.player).count()
        return number_of_cards

    def get_total_likes(self):
        return self.number_likes

    def get_card_owner(self):
        return self.owner

    def save(self, *args, **kwargs):
        value = (
            self.player.name
            + "-"
            + self.rarity.name
            + "-"
            + self.player.team.country.country.name
            + "-"
            + str(self.index)
        )  # new
        if not self.slug:
            self.slug = slugify(value, allow_unicode=False)
        return super().save(*args, **kwargs)


class PlayerCardLike(models.Model):
    playercard = models.ForeignKey(
        PlayerCard, on_delete=models.CASCADE, related_name="likes"
    )
    user = models.ForeignKey(
        "account.CustomUser", on_delete=models.CASCADE, related_name="liked_cards"
    )

    def __str__(self):
        return self.user.username
