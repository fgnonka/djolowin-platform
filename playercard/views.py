from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from auction.models import Auction
from auction.forms import AuctionForm
from auction.mixins import AuctionCreationMixin
from base.models import Player
from core.mixins import CustomDispatchMixin
from playercard.models import PlayerCard, CardRarity
from playercard.utils import list_of_cards_to_display
from playercard.signals import playercard_viewed
from transaction.utils import create_card_purchase_transaction
from wallet.models import UserWallet

from .forms import CardForm, PlayerCardSearchForm
from .mixins import PlayerCardSearchMixin
from .signals import completed_card_purchase



class UpdatePlayerCardView(LoginRequiredMixin, UpdateView):
    model = PlayerCard
    form_class = CardForm
    template_name = "djolowin/playercard/playercard_detail.html"

    def post(self, request, pk):
        playercard = get_object_or_404(PlayerCard, pk=pk, owner=request.user)
        if playercard.is_locked:
            messages.error(request, "This card is locked and cannot be Updated.")
            return redirect("playercard:playercard-detail", pk=playercard.pk)
        form = CardForm(request.POST)
        if form.is_valid():
            playercard.price = form.cleaned_data["price"]
            playercard.for_sale = form.cleaned_data["for_sale"]
            playercard.is_public = form.cleaned_data["is_public"]
            playercard.save()
        return redirect("playercard:playercard-detail", pk=playercard.pk)


class PlayerCardDetailView(CustomDispatchMixin, AuctionCreationMixin, DetailView):
    context_object_name = "playercard"
    model = PlayerCard
    view_signal = playercard_viewed
    template_name = "djolowin/playercard/playercard_detail.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Trigger the signal when the player card is viewed
        signal = self.view_signal.send(sender=self.__class__, playercard=self.object)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        past_auctions = Auction.objects.filter(
            Q(card=self.object)
            & Q(end_time__lte=timezone.now()))[:5]
        context["past_auctions"] = past_auctions
        context["past_auctions_count"] = past_auctions.count()
        context["auction_form"] = AuctionForm()
        context["form"] = CardForm(playercard_instance=self.object)
        context["active_auctions"] = Auction.objects.filter(
            Q(card=self.object)
            & Q(end_time__gte=timezone.now())
            & Q(owner=self.object.owner)
        )
        return context


class PlayerCardListView(CustomDispatchMixin, PlayerCardSearchMixin, ListView):
    """Alternative Playercard Listview"""

    model = PlayerCard
    form_class = PlayerCardSearchForm
    template_name = "djolowin/playercard/all_playercards.html"
    context_object_name = "playercards"
    paginate_by = settings.DJOLOWIN_PLAYERCARD_PAGINATE_BY
    POSITION_CHOICES = Player.POSITION_CHOICES
    RARITY_CHOICES = [(rarity.name, rarity.name) for rarity in CardRarity.objects.all()]

    def get_queryset(self):
        # The method below is to only show playercards that are for sale and that are not from the MasterTeam COllection
        form = self.form_class(self.request.GET)
        queryset = list_of_cards_to_display()
        if form.is_valid():
            queryset = self.filter_playercards(queryset)
        
        sort_by = self.request.GET.get("sort_by")
        order = self.request.GET.get("order")

        if sort_by:
            if order == "desc":
                sort_by = f"-{sort_by}"
            queryset = queryset.order_by(sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PlayerCardSearchForm(self.request.GET)
        context["rarity_choices"] = self.RARITY_CHOICES
        context["position_choices"] = self.POSITION_CHOICES
        return context


class UserPlayerCardListView(CustomDispatchMixin, PlayerCardSearchMixin, ListView):
    model = PlayerCard
    form_class = PlayerCardSearchForm
    context_object_name = "playercards"
    template_name = "djolowin/playercard/owned_playercard_list.html"
    paginate_by = settings.DJOLOWIN_PLAYERCARD_PAGINATE_BY

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        user = self.request.user
        queryset = self.model.objects.filter(owner=user)

        if form.is_valid():
            queryset = self.filter_playercards(queryset)
        
        sort_by = self.request.GET.get("sort_by")
        order = self.request.GET.get("order")

        if sort_by:
            if order == "desc":
                sort_by = f"-{sort_by}"
            queryset = queryset.order_by(sort_by)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PlayerCardSearchForm(self.request.GET)
        return context

        


def playercards_by_team_list(request, slug):
    """List of playercards owned by the user"""

    playercards = PlayerCard.objects.filter(player__team__slug=slug)
    paginator = Paginator(playercards, settings.DJOLOWIN_PLAYERCARD_PAGINATE_BY)
    page = request.GET.get("page")
    try:
        playercards = paginator.page(page)
    except PageNotAnInteger:
        playercards = paginator.page(1)
    except EmptyPage:
        playercards = paginator.page(paginator.num_pages)

    return render(
        request,
        "djolowin/playercard/playercards_by_team_list.html",
        {"playercards": playercards},
    )


@login_required
def purchase_playercard(request, pk):
    playercard = get_object_or_404(PlayerCard, pk=pk)
    user = request.user
    user_wallet = UserWallet.objects.get(user=user)

    if user_wallet.available_balance >= playercard.price:
        user_wallet.balance -= playercard.price
        user_wallet.save()
        playercard.owner = request.user
        playercard.for_sale = False
        playercard.save()
        create_card_purchase_transaction(
            user=request.user, card=playercard, amount_spent=playercard.price
        )
        messages.success(
            request,
            "Player card successfully purchased! Your balance is now {}DJOBA.".format(
                user_wallet.balance
            ),
        )

    else:
        messages.error(request, "Insufficient balance to purchase the player card.")

    return redirect("playercard:playercard-detail", pk=playercard.pk)
