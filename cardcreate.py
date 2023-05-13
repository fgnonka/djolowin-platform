import os
import django
import random

from django.utils.text import slugify
from django.core.exceptions import ValidationError


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djolowin.settings")
django.setup()

from account.models import CustomUser
from base.models import Player
from playercard.models import PlayerCard, CardRarity


# Fetch instances of the related models
owners = list(CustomUser.objects.all())
players = list(Player.objects.all())
rarities = list(CardRarity.objects.all())


# Function to generate a random image file (if needed)
def random_image():
    # Replace this with the path to a folder containing images
    images_path = "/path/to/images/"
    random_image = random.choice(os.listdir(images_path))
    return os.path.join(images_path, random_image)


def create_playercards():
    for player in players:
        for i in range(250):
            owner = None
            common_rarity = CardRarity.objects.get(name="Common")
            common_price = random.randint(0, 100)
            playercard_common = PlayerCard(
                for_sale=True,
                is_public=True,
                owner=owner,
                player=player,
                rarity=common_rarity,
                price=common_price,
                index=i,
                slug=slugify(f"{player.name}-{common_rarity}-{i}"),
                number_likes=random.randint(0, 100),
            )
            playercard_common.save()
            print(f"PlayerCard {playercard_common.slug} created successfully!")
        
        for i in range(101):
            owner = None
            limited_rarity = CardRarity.objects.get(name="Limited")
            limited_price = random.randint(1000, 2500)
            playercard_limited = PlayerCard(
                for_sale=True,
                is_public=True,
                owner=owner,
                player=player,
                rarity=limited_rarity,
                price=limited_price,
                index=i,
                slug=slugify(f"{player.name}-{limited_rarity}-{i}"),
                number_likes=random.randint(0, 100),
            )
            playercard_limited.save()
            print(f"PlayerCard {playercard_limited.slug} created successfully!")
            
        for i in range(51):
            owner = None
            rare_rarity = CardRarity.objects.get(name="Rare")
            rare_price = random.randint(2500, 5000)
            playercard_rare = PlayerCard(
                for_sale=True,
                is_public=True,
                owner=owner,
                player=player,
                rarity=rare_rarity,
                price=rare_price,
                index=i,
                slug=slugify(f"{player.name}-{rare_rarity}-{i}"),
                number_likes=random.randint(0, 100),
            )
            playercard_rare.save()
            print(f"PlayerCard {playercard_rare.slug} created successfully!")
            
        for i in range(11):
            owner = None
            super_rare_rarity = CardRarity.objects.get(name="Super Rare")
            super_rare_price = random.randint(5000, 10000)
            playercard_super_rare = PlayerCard(
                for_sale=True,
                is_public=True,
                owner=owner,
                player=player,
                rarity=super_rare_rarity,
                price=super_rare_price,
                index=i,
                slug=slugify(f"{player.name}-{super_rare_rarity}-{i}"),
                number_likes=random.randint(0, 100),
            )
            playercard_super_rare.save()
            print(f"PlayerCard {playercard_super_rare.slug} created successfully!")
        
        for i in range(2):
            owner = None
            unique_rarity = CardRarity.objects.get(name="Unique")
            unique_price = 100000
            playercard_unique = PlayerCard(
                for_sale=True,
                is_public=True,
                owner=owner,
                player=player,
                rarity=unique_rarity,
                price=unique_price,
                index=i,
                slug=slugify(f"{player.name}-{unique_rarity}-{i}"),
                number_likes=random.randint(0, 100),
            )
            playercard_unique.save()
            print(f"PlayerCard {playercard_unique.slug} created successfully!")

if __name__ == "__main__":
    create_playercards()
