from django import forms

from playercard.models import CardRarity
from .models import Bundle


class BundleForm(forms.ModelForm):
    class Meta:
        model = Bundle
        fields = "__all__"


class BundlePurchaseForm(forms.Form):
    RARITY_CHOICES = (
        ("Common", "Common"),
        ("Rare", "Rare"),
    )
    rarity = forms.ChoiceField(choices=RARITY_CHOICES)


class BundleFilterForm(forms.Form):
    RARITY_CHOICES = [(rarity.name, rarity.name) for rarity in CardRarity.objects.all()]
    rarity = forms.ChoiceField(
        required=False,
        choices=RARITY_CHOICES,
        label="Rarity",
        widget=forms.Select(attrs={"class": "custom-select"}),
    )

    def filter_queryset(self, queryset):
        filter_kwargs = {
            key: value for key, value in self.cleaned_data.items() if value is not None
        }
        return queryset.filter(**filter_kwargs) if filter_kwargs else queryset