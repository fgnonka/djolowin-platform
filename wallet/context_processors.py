from .models import UserWallet

def user_balance(request):
    context = {}
    if request.user.is_authenticated:
        user_wallet = UserWallet.objects.get(user=request.user)
        return {"available_balance": user_wallet.available_balance}
    return context