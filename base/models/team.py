from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Team(models.Model):
    name = models.CharField(max_length=55, null=True, blank=True)
    country = models.ForeignKey(
        "base.Country", on_delete=models.PROTECT, null=False, blank=False
    )
    year = models.IntegerField()
    slug = models.SlugField(
        max_length=55,
        unique=True,
        help_text="Label for URL configuration",
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.name:
            return f"{self.name} --- {self.year}"
        else:
            return f"{self.country.country.name} --- {self.year}"
    def _generate_slug(self):
        name = self.name or self.country.country.name
        value = f"{name}-{self.year}"
        return slugify(value, allow_unicode=False)
    def get_absolute_url(self):
        return reverse("base:team-players-list", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_slug()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["year"]
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        unique_together = ("name", "country", "year")