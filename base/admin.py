from django.contrib import admin

# Register your models here.
from base.models import Country, Player, Team

@admin.register(Country)

class CountryAdmin(admin.ModelAdmin):
    list_display = ['country', 'id', ]
    
admin.site.register(Player)
@admin.register(Team)

class TeamAdmin(admin.ModelAdmin):
    list_display = ['slug', 'id', ]