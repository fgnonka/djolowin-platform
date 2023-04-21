from django.urls import path, include

from .views import user_wallet_balance

app_name = "wallet"

urlpatterns = [
    path('dashboard',view=user_wallet_balance, name='wallet-dashboard' ),
]