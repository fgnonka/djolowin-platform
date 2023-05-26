from datetime import timedelta


from django import forms
from django.forms.widgets import DateTimeInput
from django.utils import timezone

from playercard.models import CardRarity
from .models import Auction, Bid
from wallet.models import UserWallet


class AuctionForm(forms.ModelForm):
    starting_price = forms.IntegerField(min_value=2000, required=True, label="Starting Price")
    duration = forms.IntegerField(min_value=1, max_value=24, required=True, label="Auction duration (in hours)")
    class Meta:
        model = Auction
        fields = ["starting_price", "duration"]
        widgets = {
            "starting_price": forms.NumberInput(attrs={"step": "100.00"}),
            "duration": forms.NumberInput(attrs={"step": "1.00", "max": "24.00"}),
        }
        
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["duration"].min = 1

    def clean_duration(self):
        duration = self.cleaned_data.get("duration")
        if duration < 1:
            raise forms.ValidationError(
                "The auction must last for at least 1 hour."
            )
        elif duration > 24:
            raise forms.ValidationError(
                "The auction must last for at most 24 hours."
            )
        return duration


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]
        widgets = {
            "amount": forms.NumberInput(attrs={"step": "100.00", "min": "0.00"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get("amount")
        if amount is None:
            raise forms.ValidationError("Please enter an amount.")

        return cleaned_data

class AuctionSearchForm(forms.Form):
    RARITY_CHOICES = [ (rarity.name, rarity.name) for rarity in CardRarity.objects.all() ]
    
    card_name = forms.CharField(required=False, label="Card name")
    team_name = forms.CharField(required=False, label="Team name")
    rarity = forms.ChoiceField(required=False, label="Rarity", choices=[(None, "Any rarity")] + RARITY_CHOICES)
    ending_soon = forms.BooleanField(required=False, label="Ending soon")
