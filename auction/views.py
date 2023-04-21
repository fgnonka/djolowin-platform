from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.utils import timezone

from playercard.models import PlayerCard
from .models import Auction, Bid
from .forms import AuctionForm, BidForm
from .mixins import BidFormMixin


class ActiveAuctionListView(LoginRequiredMixin, ListView):
    model = Auction
    template_name = "djolowin/auction/active_auctions.html"
    context_object_name = "auctions"
    
    def get_queryset(self):
        now = timezone.now()
        active_auctions = Auction.objects.filter(Q(start_time__lte=now) & Q(end_time__gte=now))
        return active_auctions


@login_required
def create_auction(request, card_pk):
    card = get_object_or_404(PlayerCard, pk=card_pk)
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.card = card
            auction.owner = request.user
            try:
                # auction.start_time = timezone.make_aware(auction.start_time)
                auction.save()
            except IntegrityError:
                messages.error(request, "You already have an active auction for this card.")
                return redirect("playercard:playercard-detail", pk=card.pk)
            return redirect("auction:auction_detail", pk=auction.pk)
    else:
        form = AuctionForm()
    return render(request, "djolowin/auction/create_auction.html", {"form": form, "card": card})


class AuctionDetailView(LoginRequiredMixin, DetailView, BidFormMixin):
    model = Auction
    template_name = "djolowin/auction/auction_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bid_form"] = BidForm()
        context["auction"] = Auction.objects.get(pk=self.kwargs["pk"])
        
        return context


