from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin

from wallet.models import UserWallet
from .forms import BidForm
from .models import Bid
from .utils import add_watcher, increase_number_of_bids


class BidFormMixin(SingleObjectMixin):
    def dispatch(self, request, *args, **kwargs):
        with transaction.atomic():
            response = super().dispatch(request, *args, **kwargs)
            return response

    def post(self, request, *args, **kwargs):
        auction = self.get_object()
        previous_bid = auction.get_highest_bid()
        form = BidForm(request.POST)

        if form.is_valid():
            bid_amount = form.cleaned_data["amount"]
            bidder = request.user
            bid = Bid(auction=auction, bidder=bidder, amount=bid_amount)
            if auction.accept_bid(bidder, bid_amount):
                add_watcher(bidder, auction)
                if previous_bid:
                    previous_bidder = previous_bid.bidder
                    previous_bidder_wallet = UserWallet.objects.get(user=previous_bidder)
                    previous_bidder_wallet.reserved_balance -= previous_bid.amount
                    previous_bidder_wallet.save()
                bid.save()
                increase_number_of_bids(auction)
                
                messages.success(
                    request,
                    "Your bid of {} has been accepted.".format(bid_amount),
                )
                if previous_bid and previous_bidder != bidder:
                    send_mail(
                        "Your bid has been outbid",
                        f"Someone has outbid you on {auction}. Visit the auction page to place a new bid.",
                        "noreply@djolo.win",
                        [previous_bidder.email],
                        fail_silently=False,
                    )
                return redirect(reverse("auction:active_auctions", ))
            else:
                messages.info(
                    request,
                    f"""The amount of {bid_amount} you entered is invalid. 
                    It could be that you do not have enough funds in your wallet, 
                    or that the amount is lower than the current bid.""",
                )
                return redirect(reverse("auction:active_auctions", ))

        return self.render_to_response(self.get_context_data(bid_form=form))
