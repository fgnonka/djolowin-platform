from datetime import timedelta


from django import forms
from django.forms.widgets import DateTimeInput
from django.utils import timezone

from .models import Auction, Bid
from wallet.models import UserWallet


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ["starting_price", "end_time"]
        widgets = {
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["end_time"].input_formats = ["%Y-%m-%dT%H:%M"]

    def clean_end_time(self):
        end_time = self.cleaned_data.get("end_time")
        if end_time and end_time < timezone.now() + timedelta(minutes=5):
            raise forms.ValidationError(
                "The auction must be active for at least 5 minutes."
            )
        return end_time


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]
        widgets = {
            "amount": forms.NumberInput(attrs={"step": "100.00"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get("amount")
        auction = self.initial.get("auction")

        return cleaned_data

class AuctionSearchForm(forms.Form):
    card_name = forms.CharField(required=False, label="Card name")
    min_end_time = forms.DateTimeField(required=False, label="Ending after", widget=DateTimeInput(attrs={'type': 'datetime-local'}))
