from django.db.models import Q


class PlayerCardSearchMixin:
    """Mixin for PlayerCardList view to filter and sort the queryset"""

    def filter_playercards(self, queryset):
        """Filter the queryset based on the search form"""
        # form = self.form_class(self.request.GET)
        # if form.is_valid():
        #     card_name = form.cleaned_data.get("card_name")
        #     team_name = form.cleaned_data.get("team_name")
        #     position = form.cleaned_data.get("position")
        #     rarity = form.cleaned_data.get("rarity")
        #     queryset = queryset.filter(
        #         Q(player__name__icontains=card_name)
        #         | Q(player__team__slug__icontains=team_name)
        #         | Q(player__position__icontains=position)
        #         | Q(rarity__name__icontains=rarity)
        #     )
        # return queryset

        if self.request.GET.get("card_name"):
            queryset = queryset.filter(
                player__name__icontains=self.request.GET.get("card_name")
            )
        if self.request.GET.get("team_name"):
            queryset = queryset.filter(
                player__team=self.request.GET.get("team_name")
            )
        if self.request.GET.get("position"):
            queryset = queryset.filter(
                player__position__icontains=self.request.GET.get("position")
            )
        if self.request.GET.get("rarity"):
            queryset = queryset.filter(
                rarity__name=self.request.GET.get("rarity")
            )
        if self.request.GET.get("price_max"):
            queryset = queryset.filter(
                price__lte=self.request.GET.get("price_max")
            )
        return queryset