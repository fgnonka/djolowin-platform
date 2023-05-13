import os
import django
from django.core.exceptions import ValidationError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djolowin.settings")
django.setup()

from base.models import Player, Team, Country

position_choices = tuple(Player.POSITION_CHOICES)
print(position_choices)

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
    for i in range(1, 24):
        position = position_choices[0][0]
        if i <= 5:
            position = position_choices[3][0]
        elif i <= 13:
            position = position_choices[1][0]
        elif i <= 21:
            position = position_choices[2][0]
        player_data = [
        {
            "name": f"South African Player {i}",
            "date_of_birth": f"1980-01-{str(i).zfill(2)}",
            "jersey_number": f"{i}",
            "position": position,
            "image": None,
            "team_id": 4,  # Replace with the actual team ID
            "country_id": 4,  # Replace with the actual country ID
            "slug": f"player-south-africa-{i}",
        }
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
