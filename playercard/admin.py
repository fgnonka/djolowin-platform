from django.contrib import admin
from .models import PlayerCard, CardRarity, PlayerCardLike
# Register your models here.
admin.site.register(CardRarity)
admin.site.register(PlayerCardLike)


@admin.register(PlayerCard)
class PlayerCardAdmin(admin.ModelAdmin):
    list_display = ("owner","player", "rarity", "slug", "price", "date_created", "date_updated")
    list_filter = ("rarity", "player__team", "for_sale")
    list_editable = ("price",)
    search_fields = ("player", "description")
    ordering = ("-date_created",)
