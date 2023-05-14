from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from account.decorators import user_is_active
from base.models import Team, Player
from playercard.models import PlayerCard, CardRarity
from playercard.utils import list_of_cards_to_display


@user_is_active
@login_required
def homeview(request):
    playercards = list_of_cards_to_display("homeview")

    context = {
        "playercards": playercards,
    }
    return render(request, "djolowin/base/home.html", context)

class HomeView(View):
    pass

def search(request):
    query = request.GET.get('q')
    team = request.GET.get('team.id')
    position = request.GET.get('position')
    rarity = request.GET.get('rarity')

    card_results = PlayerCard.objects.filter(
        Q(name__icontains=query) | Q(player__team__icontains=query) if query else Q(),
        Q(player__team__id=team) if team else Q(),
        Q(player__position=position) if position else Q(),
        Q(rarity__name=rarity) if rarity else Q(),
    )
    teams = Team.objects.all()
    positions = Player. POSITION_CHOICES
    rarities = CardRarity.objects.all()
    context = {
        'card_results': card_results,
        'request': request,
        'teams': teams,
        'positions': positions,
        'rarities': rarities,
    }

    return render(request, 'djolowin/base/search_results.html', context)