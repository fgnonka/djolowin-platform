from django.http import JsonResponse
from .models import PlayerCard


def search_player_cards(request):
    query = request.GET.get('q')
    if query:
        cards = PlayerCard.objects.filter(name__icontains=query)
        results = [{'id': card.id, 'name': card.name} for card in cards]
        return JsonResponse({'results': results})
    else:
        return JsonResponse({'results': []})
