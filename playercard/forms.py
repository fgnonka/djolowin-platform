from django import forms


from .models import CardRarity, PlayerCard
from base.models import Team, Player


class CardForm(forms.ModelForm):
    price = forms.DecimalField(decimal_places=2, max_digits=10)
    for_sale = forms.BooleanField(required=False)
    is_public = forms.BooleanField(required=False, label="Make my card public")

    class Meta:
        model = PlayerCard
        fields = ["price", "for_sale", "is_public"]

    def __init__(self, *args, **kwargs):
        self.playercard_instance = kwargs.pop("playercard_instance", None)
        super().__init__(*args, **kwargs)

        if self.playercard_instance:
            self.fields["price"].initial = self.playercard_instance.price
            self.fields["for_sale"].initial = self.playercard_instance.for_sale
            self.fields["is_public"].initial = self.playercard_instance.is_public


TEAM_CHOICES = [(int(team.id), team) for team in Team.objects.all()]
POSITION_CHOICES = [(position) for position in Player.POSITION_CHOICES]



class PlayerCardSearchForm(forms.Form):
    
    RARITY_CHOICES = [(rarity.name, rarity.name) for rarity in CardRarity.objects.all()]

    card_name = forms.CharField(required=False, label="Card name")
    team_name = forms.ChoiceField(required=False, label="Team name", choices=[(None, "Any Team")] + TEAM_CHOICES)
    position = forms.ChoiceField(required=False, label="Position", choices=[(None, "Any Position")] + POSITION_CHOICES)
    rarity = forms.ChoiceField(required=False, label="Rarity", choices=[(None, "Any rarity")] + RARITY_CHOICES)
    price_max = forms.IntegerField(min_value=0, required=False, label="Maximum price")
    serial_number = forms.IntegerField(min_value=0, required=False, label="Serial number")
    
    class Meta:
        fields = ["card_name", "team_name", "position", "rarity", "price_max"]
        widgets = {
            "price_max": forms.NumberInput(attrs={"step": "5000.00", "min": "0.00"}),
        }