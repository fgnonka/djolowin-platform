from .models import Collection, CompletedCollection
from django.contrib import admin


class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "rarity", "team", "reward", "is_active")
    list_filter = ("rarity", "team", "is_active")
    search_fields = ("name", "description")
    list_editable = ("rarity","reward")
    ordering = ("name", "rarity", "team", "reward", "is_active")
    filter_horizontal = ("cards",)


admin.site.register(Collection, CollectionAdmin)
admin.site.register(CompletedCollection)