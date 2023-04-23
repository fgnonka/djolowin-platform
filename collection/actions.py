from django.db.models import Q

from playercard.models import PlayerCard
from wallet.models import UserWallet


def has_user_completed_collection(user, collection):
    user_cards = user.playercards.all()
    cards_in_collection = collection.cards.all()
    user_cards_in_collection = user_cards.filter(
        Q(player__team=collection.team) & Q(rarity=collection.rarity)
    ).distinct("player")
    missing_cards = cards_in_collection.exclude(
        player__in=user_cards_in_collection.values_list("player", flat=True)
    )
    return len(missing_cards) == 0 and len(user_cards_in_collection) > 0


def get_collection_progress(user, collection):
    user_cards = user.playercards.all()
    cards_in_collection = collection.cards.all()
    user_cards_in_collection = user_cards.filter(
        Q(player__team=collection.team) & Q(rarity=collection.rarity)
    ).distinct("player")
    missing_cards = cards_in_collection.exclude(
        player__in=user_cards_in_collection.values_list("player", flat=True)
    )
    progress = len(user_cards_in_collection) / len(cards_in_collection) * 100
    return {
        "progress": progress,
        "user_cards": user_cards_in_collection,
        "missing_cards": missing_cards,
    }


def user_acquired_new_card(user, card):
    # Whenever a user acquires a new card, call this function
    # Assuming the card has been added to the user's collection
    # Check for the collections the card belongs to
    collections_with_card = card.collections_set.all()

    for collection in collections_with_card:
        if has_user_completed_collection(user, collection):
            # User has completed the collection
            # Give the user the reward
            check_and_release_reward(user, collection)
        else:
            # User has not completed the collection
            # Do nothing
            pass


def check_and_release_reward(user, collection):
    # Lock the cards in the collection so they can't be traded anymore
    cards_to_lock = select_cards_to_lock(user, collection)
    # Give the user the reward
    release_reward(user, collection, cards_to_lock)
    lock_cards(cards_to_lock)


def release_reward(user, collection, cards_to_lock):
    # Establish the amount of reward to give based on the collection
    reward_amount = collection.reward.amount
    # Query the user's wallet and add the reward to it'
    wallet = UserWallet.objects.get(user=user)
    wallet.balance += reward_amount
    wallet.save()


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
