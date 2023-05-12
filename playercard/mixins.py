from django.db.models import Q



class PlayerCardListMixin:
    """ Mixin for PlayerCardList view to filter and sort the queryset"""
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        rarity = self.request.GET.get("rarity")
        team = self.request.GET.get("team")
        position = self.request.GET.get("position")
        print(search, rarity, team, position)

        query = Q()
        if search:
            query &= Q(player__name__icontains=search)
        if rarity:
            query &= Q(rarity__name=rarity)
        if team:
            query &= Q(player__team__id=team)
        if position:
            query &= Q(player__position=position)

        # sort_by = self.request.GET.get("sort_by")
        # order = self.request.GET.get("order")
        queryset = queryset.filter(query)

        # if sort_by:
        #     if order == "desc":
        #         sort_by = f"-{sort_by}"
        # queryset = queryset.filter(query).order_by(sort_by)
        if rarity:
            queryset = queryset.filter(rarity__name=rarity)
            
        return queryset