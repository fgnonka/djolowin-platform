from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from base.models import Player, Team
from django.shortcuts import render


class PlayerListView(ListView):
    model = Player
    context_object_name = "list_players"
    template_name = "djolowin/base/players_list_by_teams.html"

    def get_queryset(self):
        self.team = get_object_or_404(Team, slug=self.kwargs["slug"])
        return Player.objects.filter(team=self.team)

    # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
    #     return super().get_context_data(**kwargs)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context["team"] = self.team
        return context



class PlayerDetailView(DetailView):
    model = Player
    context_object_name = "player"
    template_name = "djolowin/base/player_detail.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Player, slug=self.kwargs['slug'])
