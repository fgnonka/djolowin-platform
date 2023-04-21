from django.views.generic import ListView
from base.models import Country


class CountryListView(ListView):
    model = Country
    context_object_name = "list_countries"
