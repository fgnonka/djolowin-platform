
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import UserWallet

@login_required
def user_wallet_balance(request):
    user_wallet = get_object_or_404(UserWallet, user=request.user)
    
    context = {
        "wallet": user_wallet,
    }
    return render(request, "djolowin/wallet/wallet_dashboard.html", context)