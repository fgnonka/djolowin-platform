import os
import django
from django.core.exceptions import ValidationError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djolowin.settings")
django.setup()

from base.models import Player, Team, Country


def create_player(
    name, position, date_of_birth, jersey_number, image, team, country, slug
):
    try:
        player = Player(
            name=name,
            position=position,
            date_of_birth=date_of_birth,
            jersey_number=jersey_number,
            image=image,
            team=team,
            country=country,
            slug=slug,
        )
        player.full_clean()
        player.save()
        print(f"Player {name} created successfully!")
    except ValidationError as e:
        print(f"Failed to create player {name}. Error: {e}")


def main():
    # Replace the following example data with your actual player data
    player_data = [
        {
            "name": f"Egyptian Player {i}",
            "position": "FW"
            if i <= 5
            else "MID"
            if i <= 13
            else "DEF"
            if i <= 21
            else "GK",
            "date_of_birth": f"1993-01-{str(i).zfill(2)}",
            "jersey_number": f"{i}",
            "image": None,
            "team_id": 2,  # Replace with the actual team ID
            "country_id": 2,  # Replace with the actual country ID
            "slug": f"player-Egypt-{i}",
        }
        for i in range(1, 24)
    ]
    for player_info in player_data:
        team = Team.objects.get(pk=player_info["team_id"])
        country = Country.objects.get(pk=player_info["country_id"])
        create_player(
            name=player_info["name"],
            position=player_info["position"],
            date_of_birth=player_info["date_of_birth"],
            jersey_number=player_info["jersey_number"],
            image=player_info["image"],
            team=team,
            country=country,
            slug=player_info["slug"],
        )


if __name__ == "__main__":
    main()
