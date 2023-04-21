from django.urls import path, include
from .views import TransactionListView

app_name = "transaction"

urlpatterns = [
    path("all/", TransactionListView.as_view(), name="history"),
]
