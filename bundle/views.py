from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect

from django.views.generic import ListView, DetailView
from django.views import View

from .models import Bundle
from transaction.utils import create_bundle_purchase_transaction
from wallet.models import UserWallet


class BundleListView(ListView):
    model = Bundle
    paginate_by = 10
    context_object_name = "bundles"
    template_name = "djolowin/bundle/card_bundle_list.html"


class PurchaseBundleView(LoginRequiredMixin, View):
    template_name = "djolowin/bundle/bundle_purchase.html"

    def get(self, request, *args, **kwargs):
        bundle_id = kwargs.get("bundle_id")
        bundle = get_object_or_404(Bundle, pk=bundle_id)
        return render(request, self.template_name, {"bundle": bundle})

    def post(self, request, *args, **kwargs):
        bundle_id = kwargs.get("bundle_id")
        bundle = get_object_or_404(Bundle, id=bundle_id)
        user_wallet = UserWallet.objects.get(user=request.user)

        if user_wallet.available_balance >= bundle.price:
            user_wallet.balance -= bundle.price
            user_wallet.save()

            for card in bundle.cards.all():
                card.owner = request.user
                card.save()

            bundle.mark_as_sold(buyer=request.user)
            create_bundle_purchase_transaction(
                user=request.user, bundle=bundle, amount_spent=bundle.price
            )
            messages.success(request, "Bundle purchased successfully!")
            return redirect("bundle:bundles_list")
        else:
            messages.error(request, "Insufficient balance to purchase this bundle.")
            return render(request, self.template_name, {"bundle": bundle})


class BundleDetailView(DetailView):
    model = Bundle
    context_object_name = "bundle"
    template_name = "djolowin/bundle/bundle_detail.html"