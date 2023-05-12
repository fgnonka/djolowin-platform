from django.urls import re_path
from . import views
from .views.country_views import CountryListView
from .views.player_views import PlayerListView, PlayerDetailView
from .views.base_views import homeview, search


app_name = "base"  # here for namespacing of urls.

# map url path to function in views folder
urlpatterns = [
    re_path(r"^$", homeview, name="home"),
    re_path(r"^countries/$", CountryListView.as_view(), name="country-list"),
    re_path(
        r"^team-players/(?P<slug>[-\w]+)/$",
        PlayerListView.as_view(),
        name="team-players-list",
    ),
    re_path(
        r"^player/(?P<slug>[-\w]+)/$",
        PlayerDetailView.as_view(),
        name="player-detail",
    ),
]
