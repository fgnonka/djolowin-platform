import datetime

from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Player(models.Model):
    POSITION_CHOICES = (
        ("GK", "Goalkeeper"),
        ("DEF", "Defender"),
        ("MID", "Midfielder"),
        ("FW", "Forward"),
    )
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=3, choices=POSITION_CHOICES)
    date_of_birth = models.DateField()
    jersey_number = models.PositiveIntegerField()
    image = models.ImageField(upload_to="uploads/players", null=True, blank=True)
    team = models.ForeignKey(
        "base.Team", on_delete=models.SET_NULL, null=True, blank=True
    )
    country = models.ForeignKey(
        "base.Country", on_delete=models.SET_NULL, blank=True, null=True
    )
    slug = models.SlugField(
        max_length=155,
        help_text="Label for URL configuration",
        null=True,
        blank=True,
        unique=True,
    )

    def __str__(self):
        return f"{self.name} --- {self.position} --- {self.team}"

    @staticmethod
    def get_all_players():
        return Player.objects.all()

    @staticmethod
    def get_all_players_by_team(team):
        if team:
            return Player.objects.filter(team=team)
        else:
            return Player.objects.all()
        
    @property
    def get_player_age(self):
        team_year = self.team.year
        player_age = team_year - self.date_of_birth.year
        return player_age
    
    @property
    def get_player_position_verbose(self):
        return dict(Player.POSITION_CHOICES)[self.position]

    def _generate_slug(self):
        value = f"{self.name}-{self.team.country.country.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_slug()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("base:player-detail", kwargs={"slug": self.slug})
