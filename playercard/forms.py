from django import forms

from .filters import PlayerCardFilter
from .models import CardRarity, PlayerCard
from base.models import Team

class PriceForm(forms.Form):
    price = forms.DecimalField(decimal_places=2, max_digits=10)
    

RARITY_CHOICES = [(rarity.name, rarity.name) for rarity in CardRarity.objects.all()]
TEAM_CHOICES = [(team.name, team.name) for team in Team.objects.all()]
POSITION_CHOICES = [(position) for position in PlayerCard.POSITIONS]
class PlayerCardFilterForm(forms.Form):
    name = forms.CharField(
        required=False,
        label="Player Name",
        widget=forms.TextInput(attrs={"placeholder": "Player name"}),
    )
    rarity = forms.ChoiceField(
        required=False,
        choices=RARITY_CHOICES,
        label="Rarity",
        widget=forms.Select(attrs={"class": "custom-select"}),
    )
    team = forms.MultipleChoiceField(
        required=False,
        choices=TEAM_CHOICES,
        label="Team",
        widget=forms.CheckboxSelectMultiple(),
    )
    position = forms.MultipleChoiceField(
        required=False,
        choices=POSITION_CHOICES,
        label="Position",
        widget=forms.CheckboxSelectMultiple(),
    )


    def filter_queryset(self, queryset):
        filter_kwargs = {
            key: value for key, value in self.cleaned_data.items() if value is not None
        }
        return PlayerCardFilter(filter_kwargs, queryset=queryset).qs