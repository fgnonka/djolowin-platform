from django.contrib import admin
from .models import PlayerCard, CardRarity, PlayerCardLike

# Register your models here.
admin.site.register(CardRarity)
admin.site.register(PlayerCardLike)


@admin.register(PlayerCard)
class PlayerCardAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "player",
        "rarity",
        "slug",
        "price",
        "date_created",
        "date_updated",
        "is_locked",
    )
    list_filter = ("rarity", "player__team", "for_sale", "is_locked")
    list_editable = ("price","is_locked")
    search_fields = ("player", "description")
    ordering = ("-date_created",)
