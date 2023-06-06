from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

from auction.models import Auction, Bid
from bundle.models import Bundle
from transaction.models import Transaction, AuctionTransaction, InAppCurrencyTransaction


class DjolowinProfileView(LoginRequiredMixin, TemplateView):
    template_name = "djolowin/djolowin_profile/djolowin_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_active_auctions = Auction.objects.filter(
            Q(owner=self.request.user) & Q(auction_ended=False)
        ).order_by("-timestamp")
        my_bids = Bid.objects.filter(Q(bidder=self.request.user)).order_by("-timestamp")
        my_card_purchases = Transaction.objects.filter(
            Q(buyer=self.request.user) & Q(transaction_type="card_purchase")
        ).order_by("-timestamp")
        my_bundle_purchases = Transaction.objects.filter(
            Q(buyer=self.request.user) & Q(transaction_type="bundle_purchase")
        ).order_by("-timestamp")
        my_card_sales = Transaction.objects.filter(
            Q(seller=self.request.user) & Q(transaction_type="card_purchase")
        ).order_by("-timestamp")
        my_currency_purchases = InAppCurrencyTransaction.objects.filter(
            Q(user=self.request.user)
        ).order_by("-timestamp")
        my_auction_purchases = AuctionTransaction.objects.filter(
            Q(winner=self.request.user)
        ).order_by("-timestamp")
        latest_activity = sorted(
            list(my_active_auctions)
            + list(my_bids)
            + list(my_card_purchases)
            + list(my_bundle_purchases)
            + list(my_card_sales)
            + list(my_currency_purchases)
            + list(my_auction_purchases),
            key=lambda x: x.timestamp,
            reverse=True,
        )[:10]

        context["latest_activity"] = latest_activity
        context["my_active_auctions"] = my_active_auctions
        context["my_bids"] = my_bids
        context["my_card_purchases"] = my_card_purchases
        context["my_bundle_purchases"] = my_bundle_purchases
        context["my_card_sales"] = my_card_sales
        context["my_currency_purchases"] = my_currency_purchases
        context["my_auction_purchases"] = my_auction_purchases
        return context
