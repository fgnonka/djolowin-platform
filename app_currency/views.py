from django.views.generic import ListView

from .models import CurrencyPackage


class CurrencyPackageListView(ListView):
    model = CurrencyPackage
    template_name = "djolowin/app_currency/currency_package_list.html"
    context_object_name = "currency_packages"

