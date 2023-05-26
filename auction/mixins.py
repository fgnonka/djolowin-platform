from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin

from communication.notifications.actions import send_notification
from transaction.utils import create_auction_transaction
from wallet.models import UserWallet

from .forms import BidForm, AuctionForm
from .models import Bid
from .utils import add_watcher, increase_number_of_bids
from .signals import bid_submitted


class BidFormMixin(SingleObjectMixin):
    def dispatch(self, request, *args, **kwargs):
        with transaction.atomic():
            response = super().dispatch(request, *args, **kwargs)
            return response

    def post(self, request, *args, **kwargs):
        auction = self.get_object()
        print(auction)
        previous_bid = auction.get_highest_bid()
        form = BidForm(request.POST)

        if form.is_valid():
            bid_amount = form.cleaned_data["amount"]
            bidder = request.user
            bid = Bid(auction=auction, bidder=bidder, amount=bid_amount)
            if bidder == auction.owner:
                messages.error(request, "You cannot bid on your own auction.")
                return redirect("auction:auction-detail", pk=auction.pk)
            if auction.accept_bid(bidder, bid_amount):
                add_watcher(bidder, auction)
                if previous_bid:
                    if previous_bid.bidder == bidder:
                        messages.error(
                            request, "You have already placed the highest bid."
                        )
                        return redirect(
                            "auction:auction-detail", pk=auction.pk
                        )
                    previous_bidder = previous_bid.bidder
                    previous_bidder_wallet = UserWallet.objects.get(
                        user=previous_bidder
                    )
                    previous_bidder_wallet.reserved_balance -= previous_bid.amount
                    previous_bidder_wallet.save()
                bid.save()
                increase_number_of_bids(auction)
                bid_submitted.send(sender=self.__class__, bid=bid)

                messages.success(
                    request,
                    "Your bid of {} has been accepted.".format(bid_amount),
                )
                # Notify the owner of the auction
                send_notification(
                    recipient=auction.owner,
                    subject="New bid on {}".format(auction),
                    message="{} has placed a bid of {} DJOBA on your auction for {}.".format(
                        bidder, bid_amount, auction
                    ),
                )
                # Notify the previous bidder if there was one
                if previous_bid and previous_bidder != bidder:
                    send_notification(
                        recipient=previous_bidder,
                        subject="Bid on {} has been outbid".format(auction),
                        message="Your bid of {} DJOBA on {} has been outbid by {}.".format(
                            previous_bid.amount, auction, bidder
                        ),
                    )
                # Notify the watchers
                watchers = auction.watchers.all().exclude(
                    Q(username=bidder.username)
                    & Q(username = auction.owner.username)
                    & Q(username=previous_bidder.username if previous_bid else None)
                )
                for watcher in watchers:
                    send_notification(
                        recipient=watcher,
                        subject="New bid on {}".format(auction),
                        message="{} has placed a bid of {} on {}.".format(
                            bidder, bid_amount, auction
                        ),
                    )
            else:
                messages.info(
                    request,
                    f"""The amount of {bid_amount} DJOBA you entered is invalid. 
                    It could be that you do not have enough funds in your wallet, 
                    or that the amount is lower than the current bid.""",
                )
                return redirect(
                    reverse(
                        "auction:active_auctions",
                    )
                )
        return redirect(
            reverse(
                "auction:auction_detail",
                kwargs={"pk": auction.pk},
            )
        )


class AuctionSearchMixin:
    def filter_auctions(self, auctions):
        now = timezone.now()
        if self.request.GET.get("ending_soon"):
            auctions = auctions.filter(
                Q(end_time__gte=now)
                & Q(end_time__lte=now + timezone.timedelta(hours=1))
            )
        if self.request.GET.get("rarity"):
            auctions = auctions.filter(
                card__rarity__name=self.request.GET.get("rarity")
            )

        if self.request.GET.get("card_name"):
            auctions = auctions.filter(
                card__player__name__icontains=self.request.GET.get("card_name")
            )
        if self.request.GET.get("team_name"):
            auctions = auctions.filter(
                card__player__team__slug__icontains=self.request.GET.get("team_name")
            )
        return auctions


class AuctionCreationMixin(SingleObjectMixin):
    def dispatch(self, request, *args, **kwargs):
        with transaction.atomic():
            response = super().dispatch(request, *args, **kwargs)
            return response

    def post(self, request, *args, **kwargs):
        playercard = self.get_object()
        print(playercard)
        form = AuctionForm(request.POST)

        if form.is_valid():
            auction = form.save(commit=False)
            auction.card = playercard
            auction.owner = request.user
            playercard.for_sale = False
            playercard.is_public = False
            playercard.save()
            try:
                auction.save()
                create_auction_transaction(
                    seller=auction.owner,
                    winner=None,
                    auction=auction,
                    start_price=auction.starting_price,
                    winning_bid=None,
                    start_time=auction.start_time,
                    end_time=auction.end_time,
                    number_of_bids=0,
                    number_of_watchers=0,
                )
                auction.watchers.add(request.user)
            except IntegrityError:
                messages.error(
                    request, "You already have an auction for this card running."
                )
                return redirect("playercard:playercard_detail", pk=playercard.pk)
            messages.success(request, "Your auction has been created.")
            return redirect(
                reverse(
                    "auction:auction_detail",
                    kwargs={"pk": auction.pk},
                )
            )
