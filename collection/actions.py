from django.db.models import Q

from playercard.models import PlayerCard
from wallet.models import UserWallet
from reward.actions import release_reward

from .models import Collection
from .signals import collection_completed


def user_completed_collection(user, collection, **kwargs):
    collection = Collection.objects.get(pk=collection.pk)
    cards_to_lock = select_cards_to_lock(user, collection)
    lock_cards(cards_to_lock)


collection_completed.connect(user_completed_collection)


def get_collection_progress(user, collection):
    cards_in_collection = collection.cards.all()
    user_cards_in_collection = get_user_card_collection(user, collection)
    missing_cards = get_user_missing_cards(user, collection)
    progress = len(user_cards_in_collection) / len(cards_in_collection) * 100
    return {
        "progress": progress,
        "user_cards": user_cards_in_collection,
        "missing_cards": missing_cards,
    }


def get_user_card_collection(user, collection):
    user_cards = user.playercards.all()
    user_cards_in_collection = user_cards.filter(
        Q(player__team=collection.team) & Q(rarity=collection.rarity)
    ).distinct("player")
    return user_cards_in_collection


def get_user_missing_cards(user, collection):
    cards_in_collection = collection.cards.all()
    user_cards_in_collection = get_user_card_collection(user, collection)
    missing_cards = cards_in_collection.exclude(
        player__in=user_cards_in_collection.values_list("player", flat=True)
    )
    return missing_cards


def get_user_card_collection_quantities(user, collection):
    # Get the quantities of cards the user has in each collection
    cards_quantity = get_user_card_collection(user, collection).count()
    return cards_quantity


def lock_cards(cards_to_lock):
    for card in cards_to_lock:
        card.is_locked = True
        card.for_sale = False
        card.is_public = False
        card.save()


def select_cards_to_lock(user, collection):
    user_cards = PlayerCard.objects.filter(owner=user)
    cards_to_lock = []

    for card in collection.cards.all():
        user_card = user_cards.filter(
            player=card.player, rarity=collection.rarity
        ).first()
        if user_card and user_card not in cards_to_lock:
            cards_to_lock.append(user_card)
    return cards_to_lock
