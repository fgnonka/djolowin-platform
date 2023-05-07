from django.urls import path
from . import views

app_name = "auction"

urlpatterns = [
    path("all/", views.ActiveAuctionListView.as_view(), name="active_auctions"),
    path("create/<int:card_pk>/", views.create_auction, name="create_auction"),
    path("<int:pk>/", views.AuctionDetailView.as_view(), name="auction_detail"),
    path(
        "<int:auction_pk>/toggle_watcher/",
        views.toggle_watch,
        name="toggle_watcher",
    ),
]
