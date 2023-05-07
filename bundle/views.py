from django.contrib import messages
from  django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect

from django.views.generic import ListView, DetailView
from django.views import View

from transaction.utils import create_bundle_purchase_transaction
from wallet.models import UserWallet

from .models import Bundle
from .forms import BundleFilterForm

class BundleListView(ListView):
    model = Bundle
    paginate_by = 10
    context_object_name = "bundles"
    template_name = "djolowin/bundle/card_bundle_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_data = self.request.GET.copy()
        filter_form = BundleFilterForm(filter_data)
        context["filter_form"] = filter_form
        return context
    
    def get_queryset(self):
        queryset = Bundle.objects.filter(is_sold=False)
        filter_form = BundleFilterForm(self.request.GET)
        if filter_form.is_valid():
            rarity = filter_form.cleaned_data.get("rarity")
            queryset = queryset.filter(rarity__name=rarity)
        return queryset



@login_required
def purchase_bundle(request, bundle_id):
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
        return redirect("bundle:bundle-detail", pk=bundle.id)
    else:
        messages.error(request, "Insufficient balance to purchase this bundle.")
        # return render(request, "djolowin/bundle/bundle_purchase.html", {"bundle": bundle})
    return redirect("bundle:bundles-list")

class BundleDetailView(DetailView):
    model = Bundle
    context_object_name = "bundle"
    template_name = "djolowin/bundle/bundle_detail.html"