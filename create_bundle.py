import os
import django
import random


from django.db.models import Q

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djolowin.settings")
django.setup()
from playercard.models import PlayerCard, CardRarity
from bundle.models import Bundle


# def create_bundles():
#     # Get all card rarities
#     rarities = CardRarity.objects.all().exclude(name="Common")
#     rarity = CardRarity.objects.get(name="Limited")
#     # Loop through rarities and create bundles for each rarity
#     # for rarity in rarities:
#     # Get all available cards of the current rarity without an owner
#     available_cards = PlayerCard.objects.filter(Q(rarity=rarity) & Q(owner=None) & Q(index__gt=30))
#     bundle_index = 1
#     bundle_size = 10
#     # While there are enough cards for a bundle
#     while True:
#         if available_cards.count() >= bundle_size:
#         card_bundle = Bundle(
#             rarity=rarity,
#             name=f"{rarity.name} Bundle {bundle_index}",
#             price=50000,
#         )
#         # Randomly select cards from the available_cards queryset
#         selected_cards = random.sample(list(available_cards), bundle_size)

#         card_bundle.save()  # Save the instance to generate the ID
#         bundle_index += 1

#         for card in selected_cards:
#             Bundle.cards.through.objects.create(
#                 card_bundle=card_bundle, player_card=card
#             )

#             print(f"Card {card.slug} added to bundle {card_bundle.name}")
#         # Update the amount of available cards
#         available_cards = PlayerCard.objects.filter(Q(rarity=rarity) & Q(index__gt=30) & Q(owner=None) & ~Q(bundle__isnull=False))
#     print("Card bundles created.")


def create_bundles():
    # Get the desired rarity and higher rarities
    desired_rarity = CardRarity.objects.get(name="Common")
    higher_rarities = CardRarity.objects.all().exclude(name="Common").exclude(name="Unique").exclude(name="Super Rare")

    bundle_index = 1
    bundle_size = 10
    
    # Get all available cards of the current rarity and higher rarities without an owner
    available_cards = PlayerCard.objects.filter(Q(rarity=desired_rarity) & Q(owner=None) & Q(index__gt=30))
    # While there are enough cards for a bundle
    while available_cards.count() >= bundle_size:
        card_bundle = Bundle(
            name=f"{desired_rarity.name} Bundle {bundle_index}",
            rarity=desired_rarity,
            price=30000,
        )

        # Randomly select 7 cards of the desired rarity
        selected_cards = random.sample(list(available_cards.filter(rarity=desired_rarity)), 7)
        
        for i in range(3):
            higher_rarity = random.choice(list(higher_rarities))
            higher_rarity_cards = PlayerCard.objects.filter(Q(rarity=higher_rarity) & Q(owner=None) & Q(index__gt=15))
            selected_cards.append(random.choice(list(higher_rarity_cards)))

        card_bundle.save()  # Save the instance to generate the ID
        bundle_index += 1

        for card in selected_cards:
            Bundle.cards.through.objects.create(
                card_bundle=card_bundle, player_card=card
            )
        
        available_cards = PlayerCard.objects.filter(Q(rarity=desired_rarity) & Q(index__gt=30) & Q(owner=None) & ~Q(bundle__isnull=False))


        print(f"Card {card.slug} added to bundle {card_bundle.name}")
    print("Card bundles created.")
    


if __name__ == "__main__":
    create_bundles()
