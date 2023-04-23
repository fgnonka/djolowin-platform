from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from playercard.models import PlayerCard
from playercard.utils import list_of_cards_to_display
from account.decorators import user_is_active




@user_is_active
@login_required
def homeview(request):
    playercards = list_of_cards_to_display("homeview")

    context = {
        "playercards": playercards,
    }
    return render(request, "djolowin/base/home.html", context)


def search(request):
    query = request.GET.get('q')
    team = request.GET.get('team')
    position = request.GET.get('position')
    rarity = request.GET.get('rarity')

    card_results = PlayerCard.objects.filter(
        Q(name__icontains=query) | Q(team__icontains=query) if query else Q(),
        Q(team__icontains=team) if team else Q(),
        Q(position__icontains=position) if position else Q(),
        Q(rarity__icontains=rarity) if rarity else Q(),
    )

    context = {
        'card_results': card_results,
        'request': request,
        'teams': PlayerCard.TEAMS,
        'positions': PlayerCard.POSITIONS,
        'rarities': PlayerCard.RARITIES,
    }

    return render(request, 'djolowin/base/search_results.html', context)