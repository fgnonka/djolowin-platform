from django import forms

from .filters import PlayerCardFilter
from .models import CardRarity, PlayerCard
from base.models import Team, Player

class CardForm(forms.ModelForm):
    price = forms.DecimalField(decimal_places=2, max_digits=10)
    for_sale = forms.BooleanField(required=False)
    is_public = forms.BooleanField(required=False)
    
    class Meta:
        model = PlayerCard
        fields = ['price', 'for_sale', 'is_public']
        
    def __init__(self, *args, **kwargs):
        self.playercard_instance = kwargs.pop('playercard_instance', None)
        super().__init__(*args, **kwargs)
        
        if self.playercard_instance:
            self.fields['price'].initial = self.playercard_instance.price
            self.fields['for_sale'].initial = self.playercard_instance.for_sale
            self.fields['is_public'].initial = self.playercard_instance.is_public
    

RARITY_CHOICES = [(rarity.name, rarity.name) for rarity in CardRarity.objects.all()]
TEAM_CHOICES = [(team, team) for team in Team.objects.all()]
POSITION_CHOICES = [(position) for position in Player.POSITION_CHOICES]
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