from django.urls import path
from bundle.views import purchase_bundle, BundleListView, BundleDetailView, purchase_bundle_on_rarity

app_name = "bundle"

urlpatterns = [
    # ... other URL patterns ...
    path("all/", BundleListView.as_view(), name="bundles-list"),
    path(
        "purchase/<int:pk>/",
        purchase_bundle,
        name="bundle-purchase",
    ),
    path(
        "bundle/<int:pk>/",
        BundleDetailView.as_view(),
        name="bundle-detail",
    ),
    path("rarity/<str:rarity>/", purchase_bundle_on_rarity, name="bundle-purchase-rarity")
]
