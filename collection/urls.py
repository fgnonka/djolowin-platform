from django.urls import path
from . import views

app_name = "collection"

urlpatterns = [
    path("all/", views.CollectionListView.as_view(), name="collection_list"),
    path("detail/<int:pk>/", views.CollectionDetailView.as_view(), name="collection_detail"),
]
