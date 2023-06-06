from django.db.models import Q


class PlayerCardSearchMixin:
    """Mixin for PlayerCardList view to filter and sort the queryset"""

    def filter_playercards(self, queryset):
        """Filter the queryset based on the search form"""
        
        if self.request.GET.get("card_name"):
            queryset = queryset.filter(
                player__name__icontains=self.request.GET.get("card_name")
            )
        if self.request.GET.get("team_name"):
            queryset = queryset.filter(player__team=self.request.GET.get("team_name"))
        if self.request.GET.get("position"):
            queryset = queryset.filter(
                player__position__icontains=self.request.GET.get("position")
            )
        if self.request.GET.get("serial_number"):
            queryset = queryset.filter(index=self.request.GET.get("serial_number"))
        if self.request.GET.get("rarity"):
            queryset = queryset.filter(rarity__name=self.request.GET.get("rarity"))
        if self.request.GET.get("price_max"):
            queryset = queryset.filter(price__lte=self.request.GET.get("price_max"))
        return queryset
