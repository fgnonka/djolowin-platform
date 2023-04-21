from django.db import models

from django_countries.fields import CountryField


class Country(models.Model):
    country = CountryField()

    class Meta:
        ordering = ["country"]
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.country.name
