from django.urls import path

from .views import CurrencyPackageListView
from .purchase_views import (
    purchase_currency_package,
    purchase_success,
    purchase_cancel,
    stripe_webhook,
)

app_name = "currency"

urlpatterns = [
    path("all/", CurrencyPackageListView.as_view(), name="currency_package_list"),
    # Purchase related views
    path(
        "purchase-currency/<int:package_id>/",
        purchase_currency_package,
        name="purchase_currency_package",
    ),
    path("purchase-success/", purchase_success, name="purchase_success"),
    path("purchase-cancel/", purchase_cancel, name="purchase_cancel"),
    path("stripe-webhook/", stripe_webhook, name="stripe_webhook"),
    # ...
]
