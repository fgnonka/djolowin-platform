from django.contrib import admin

# Register your models here.
from base.models import Country, Player, Team

admin.site.register(Country)
admin.site.register(Player)
admin.site.register(Team)