import os
import django
import random


from django.db.models import Q

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djolowin.settings")
django.setup()
from playercard.models import PlayerCard, CardRarity
from bundle.models import Bundle


def create_bundles():
    # Get all card rarities
    rarities = CardRarity.objects.all()

    # Loop through rarities and create bundles for each rarity
    for rarity in rarities:
        # Get all available cards of the current rarity without an owner
        available_cards = PlayerCard.objects.filter(Q(rarity=rarity)& Q(owner=None) & Q(index__gt=0))
        bundle_index = 1
        bundle_size = 10
        # While there are enough cards for a bundle
        while available_cards.count() >= bundle_size:
            card_bundle = Bundle(
                rarity=rarity,
                name=f"{rarity.name} Bundle {bundle_index}",
            )
            # Randomly select cards from the available_cards queryset
            selected_cards = random.sample(list(available_cards), bundle_size)
            # bundle_price = sum(card.price for card in selected_cards)

            card_bundle.save()  # Save the instance to generate the ID
            bundle_index += 1

            for card in selected_cards:
                Bundle.cards.through.objects.create(
                    card_bundle=card_bundle, player_card=card
                )

                print(f"Card {card.slug} added to bundle {card_bundle.name}")
            # Update the amount of available cards
            available_cards = PlayerCard.objects.filter(Q(rarity=rarity) & Q(owner=None) & ~Q(bundle__isnull=False))

    print("Card bundles created.")


if __name__ == "__main__":
    create_bundles()
