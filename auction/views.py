from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.utils import timezone

from playercard.models import PlayerCard
from transaction.utils import create_auction_transaction
from .mixins import AuctionSearchMixin
from .models import Auction, Bid
from .forms import AuctionForm, BidForm, AuctionSearchForm
from .mixins import BidFormMixin
from .utils import (
    add_watcher,
    remove_watcher,
    has_existing_active_auction,
)


class ActiveAuctionListView(LoginRequiredMixin, AuctionSearchMixin, ListView):
    model = Auction
    template_name = "djolowin/auction/auction_list.html"
    context_object_name = "auctions"
    paginate_by = settings.DJOLOWIN_PLAYERCARD_PAGINATE_BY

    def get_queryset(self):
        now = timezone.now()
        active_auctions = Auction.objects.filter(
            Q(start_time__lte=now) & Q(end_time__gte=now)
        ).order_by("end_time")
        form = AuctionSearchForm(self.request.GET)
        if form.is_valid():
            active_auctions = self.filter_auctions(active_auctions)
        return active_auctions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        watched_auctions = Auction.objects.filter(
            watchers__in=[self.request.user]
        ).filter(auction_ended=False).order_by("end_time")
        context["bid_form"] = BidForm()
        context["form"] = AuctionSearchForm(self.request.GET)
        context["watched_auctions"] = watched_auctions
        return context


@login_required
def create_auction(request, card_pk):
    card = get_object_or_404(PlayerCard, pk=card_pk)
    if has_existing_active_auction(card, request.user):
        messages.error(request, "You already have an active auction for this card.")
        return redirect("playercard:playercard-detail", pk=card.pk)
    if card.is_locked:
        messages.error(request, "This card is locked and cannot be auctioned.")
        return redirect("playercard:playercard-detail", pk=card.pk)
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.card = card
            auction.owner = request.user
            card.for_sale = False
            card.is_public = False
            card.save()
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
                    request, "You already have an active auction for this card."
                )
                return redirect("playercard:playercard-detail", pk=card.pk)
            messages.success(request, "Auction created successfully.")
            return redirect("auction:auction_detail", pk=auction.pk)
    else:
        form = AuctionForm()
    return render(
        request, "djolowin/auction/create_auction.html", {"form": form, "card": card}
    )


class AuctionDetailView(LoginRequiredMixin, DetailView, BidFormMixin):
    model = Auction
    template_name = "djolowin/auction/auction_detail.html"
    """_summary_
    """

    def get_object(self, queryset=None):
        auction = Auction.objects.get(pk=self.kwargs["pk"])
        return auction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bid_form"] = BidForm(
            initial={
                "amount": self.object.current_bid
                if self.object.current_bid
                else self.object.starting_price
            }
        )

        return context


@login_required
def toggle_watch(request, auction_pk):
    auction = get_object_or_404(Auction, pk=auction_pk)
    if request.user in auction.watchers.all():
        remove_watcher(request.user, auction)
    else:
        add_watcher(request.user, auction)
    auction.save()
    return redirect("auction:auction_detail", pk=auction.pk)


class UserAuctionView(LoginRequiredMixin, AuctionSearchMixin, ListView):
    model = Auction
    template_name = "djolowin/auction/user_auctions.html"
    context_object_name = "auctions"
    paginate_by = settings.DJOLOWIN_PLAYERCARD_PAGINATE_BY

    def get_queryset(self):
        form = AuctionSearchForm(self.request.GET)
        queryset = Auction.objects.filter(
            owner=self.request.user, end_time__gte=timezone.now()
        )
        if form.is_valid():
            queryset = self.filter_auctions(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AuctionSearchForm(self.request.GET)
        context["past_auctions"] = Auction.objects.filter(
            owner=self.request.user, auction_ended=True
        )[:4]
        return context
