from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin

from wallet.models import UserWallet
from .forms import BidForm
from .models import Bid


class BidFormMixin(SingleObjectMixin):
    def dispatch(self, request, *args, **kwargs):
        with transaction.atomic():
            response = super().dispatch(request, *args, **kwargs)
            return response

    def post(self, request, *args, **kwargs):
        auction = self.get_object()
        form = BidForm(request.POST)

        if form.is_valid():
            bid_amount = form.cleaned_data["amount"]
            bidder = request.user
            bid = Bid(auction=auction, bidder=bidder, amount=bid_amount)
            if auction.accept_bid(bidder, bid_amount):
                auction.save()
                previous_bid = auction.get_highest_bid()
                if previous_bid:
                    previous_bidder = previous_bid.bidder
                    userwallet = UserWallet.objects.get(user=previous_bidder)
                    userwallet.reserved_balance -= previous_bid.amount
                    userwallet.save()
                
                bid.save()
                messages.success(
                    request,
                    "Your bid of {} has been accepted.".format(bid_amount),
                )
                return redirect(
                    reverse("auction:auction_detail", args=[auction.pk])
                )
            else:
                messages.info(
                    request,
                    f"The amount of {bid_amount} you entered is invalid. It could be that you do not have enough funds in your wallet, or that the amount is lower than the current bid.",
                )
                return redirect(
                    reverse("auction:auction_detail", args=[auction.pk])
                )
                form.add_error("amount", "Invalid bid amount.")

        return self.render_to_response(self.get_context_data(bid_form=form))
