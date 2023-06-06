from django.urls import path, include

from .views import DjolowinProfileView

app_name = "djolowin_profile"

urlpatterns = [
    path("", DjolowinProfileView.as_view(), name="profile")
]
