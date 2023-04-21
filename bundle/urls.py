from django.urls import path
from bundle.views import PurchaseBundleView, BundleListView, BundleDetailView

app_name = "bundle"

urlpatterns = [
    # ... other URL patterns ...
    path("all/", BundleListView.as_view(), name="bundles_list"),
    path(
        "purchase/<int:bundle_id>/",
        PurchaseBundleView.as_view(),
        name="bundle_purchase",
    ),
    path(
        "bundle/<int:pk>/",
        BundleDetailView.as_view(),
        name="bundle-detail",
    ),
]
