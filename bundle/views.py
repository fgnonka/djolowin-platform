from django.contrib import messages
from  django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect

from django.views.generic import DetailView, TemplateView

from core.mixins import CustomDispatchMixin
from communication.notifications.actions import send_notification
from playercard.models import CardRarity
from transaction.utils import create_bundle_purchase_transaction
from wallet.models import UserWallet

from .models import Bundle
from .forms import BundleFilterForm

class BundleListView(CustomDispatchMixin, TemplateView):
    model = Bundle
    paginate_by = 10
    context_object_name = "bundles"
    template_name = "djolowin/bundle/card_bundle_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rarities"] = CardRarity.objects.all()
        context["common_price"]= Bundle.objects.filter(rarity__name="Common").first().get_price()
        # context["limited_price"]= Bundle.objects.filter(rarity__name="Limited").first().get_price()
        # context["rare_price"]= Bundle.objects.filter(rarity__name="Rare").first().get_price()
        return context



@login_required
def purchase_bundle(request, pk):
    bundle = get_object_or_404(Bundle, id=pk)
    user_wallet = UserWallet.objects.get(user=request.user)

    if user_wallet.available_balance >= bundle.price:
        user_wallet.balance -= bundle.price
        user_wallet.save()

        for card in bundle.cards.all():
            card.owner = request.user
            card.for_sale = False
            card.save()

        bundle.mark_as_sold(buyer=request.user)
        send_notification(recipient=request.user, subject=f"You have purchased a {bundle.rarity} Bundle!", message=f"Congratulations, You have purchased a {bundle.rarity} Bundle!")
        create_bundle_purchase_transaction(
            user=request.user, bundle=bundle, amount_spent=bundle.price
        )
        messages.success(request, "Bundle purchased successfully!")
        return redirect("bundle:bundle-detail", pk=bundle.id)
    else:
        messages.error(request, "Insufficient balance to purchase this bundle.")
        # return render(request, "djolowin/bundle/bundle_purchase.html", {"bundle": bundle})
    return redirect("bundle:bundles-list")

@login_required
def purchase_bundle_on_rarity(request, rarity):
    bundle = random_bundle(rarity=rarity)
    if bundle:
        return redirect("bundle:bundle-purchase", pk=bundle.id)
    else:
        messages.error(request, "No bundles available for this rarity.")
        return redirect("bundle:bundles-list")

def random_bundle(rarity):
    bundles = Bundle.objects.filter(rarity__name=rarity, is_sold=False)
    if bundles:
        return bundles.order_by("?").first()
    return None
class BundleDetailView(CustomDispatchMixin, DetailView):
    model = Bundle
    context_object_name = "bundle"
    template_name = "djolowin/bundle/bundle_detail.html"