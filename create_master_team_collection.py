import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djolowin.settings")
django.setup()
from django.db.models import Q
from collection.models import Collection
from playercard.models import PlayerCard, CardRarity
from base.models import Team, Player
from reward.models import DJOBAReward


def create_master_team_collection():
    # Get all teams
    teams = Team.objects.all()

    # Loop through teams and create a master team collection for each team
    for team in teams:
        rarity = "Unique"
        reward = DJOBAReward.objects.get(name=f"{rarity} Rarity Team Reward")
        # Get all available cards of the current team
        cards_to_register = PlayerCard.objects.filter(
            Q(player__team=team) & Q(index=0) & Q(rarity__name=rarity)
        )
        master_team_collection = Collection(
            name=f"{rarity} {team} Master Team Collection",
            description=f"This is the {rarity} master collection for the {team}.",
            rarity=CardRarity.objects.get(name=rarity),
            reward=reward,
            team=team,
        )
        master_team_collection.save()  # Save the instance to generate the ID

        for card in cards_to_register:
            master_team_collection.cards.add(card)
            print(
                f"Card {card.slug} added to master team collection {master_team_collection.name}"
            )

    print("Master team collections created.")


if __name__ == "__main__":
    create_master_team_collection()
