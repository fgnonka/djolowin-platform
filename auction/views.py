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
from .models import Auction, Bid
from .forms import AuctionForm, BidForm, AuctionSearchForm
from .mixins import BidFormMixin
from .utils import add_watcher, remove_watcher, has_existing_active_auction


class ActiveAuctionListView(LoginRequiredMixin, ListView):
    model = Auction
    template_name = "djolowin/auction/auction_list.html"
    context_object_name = "auctions"
    paginate_by = settings.DJOLOWIN_PLAYERCARD_PAGINATE_BY

    def get_queryset(self):
        now = timezone.now()
        active_auctions = Auction.objects.filter(
            Q(start_time__lte=now) & Q(end_time__gte=now)
        )
        form = AuctionSearchForm(self.request.GET)
        rarity = self.request.GET.get("rarity")
        if rarity:
            active_auctions = active_auctions.filter(card__rarity__name=rarity)
        if form.is_valid():
            card_name = form.cleaned_data.get("card_name")
            min_end_time = form.cleaned_data.get("min_end_time")

            if card_name:
                active_auctions = active_auctions.filter(
                    card__player__name__icontains=card_name
                )
            if min_end_time:
                active_auctions = active_auctions.filter(end_time__gte=min_end_time)
        return active_auctions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bid_form"] = BidForm()
        context["form"] = AuctionSearchForm(self.request.GET)
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
            try:
                # auction.start_time = timezone.make_aware(auction.start_time)
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
            return redirect("auction:auction_detail", pk=auction.pk)
    else:
        form = AuctionForm()
    return render(
        request, "djolowin/auction/create_auction.html", {"form": form, "card": card}
    )


class AuctionDetailView(LoginRequiredMixin, DetailView, BidFormMixin):
    model = Auction
    template_name = "djolowin/auction/auction_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["auction"] = Auction.objects.get(pk=self.kwargs["pk"])
        context["bid_form"] = BidForm()

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
