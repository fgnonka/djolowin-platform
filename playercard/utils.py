from django.db.models import Q

from .models import PlayerCard
from bundle.models import Bundle
from account.models import CustomUser


@staticmethod
def list_of_cards_to_display(name=None):
    # Get all available cards without an owner and that are not in a bundle
    available_cards = PlayerCard.objects.filter(
        index__gt=0, for_sale=True, is_locked=False, is_public=True
    ).exclude(bundle__in=Bundle.objects.all())
    # available_cards = PlayerCard.objects.filter(Q(owner=None) & Q(index__gt=0))
    if name == "homeview":
        random_display = available_cards.order_by("?")[:8]
        return random_display
    return available_cards
