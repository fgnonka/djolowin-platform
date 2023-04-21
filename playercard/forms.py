from django import forms

from .filters import PlayerCardFilter

class PriceForm(forms.Form):
    price = forms.DecimalField(decimal_places=2, max_digits=10)
    

class PlayerCardFilterForm(forms.Form):
    name = forms.CharField(required=False)
    position = forms.CharField(required=False)
    team = forms.CharField(required=False)
    rarity = forms.CharField(required=False)

    def filter_queryset(self, queryset):
        filter_kwargs = {
            key: value for key, value in self.cleaned_data.items() if value is not None
        }
        return PlayerCardFilter(filter_kwargs, queryset=queryset).qs