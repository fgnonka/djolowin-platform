from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, TemplateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from auction.models import Auction
from base.models import Team, Player
from playercard.models import PlayerCard
from playercard.utils import list_of_cards_to_display
from playercard.signals import playercard_viewed
from transaction.utils import create_card_purchase_transaction
from wallet.models import UserWallet

from .forms import PriceForm, PlayerCardFilterForm
from .filters import PlayerCardFilter


class UpdatePriceView(LoginRequiredMixin, View):
    def post(self, request, pk):
        playercard = get_object_or_404(PlayerCard, pk=pk, owner=request.user)
        form = PriceForm(request.POST)
        if form.is_valid():
            playercard.price = form.cleaned_data["price"]
            playercard.save()
        return redirect("playercard:playercard-detail", pk=playercard.pk)


class PlayerCardDetailView(DetailView):
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
        context["price_form"] = PriceForm()
        context["auction"] = Auction.objects.filter(card=self.object)
        return context


class PlayerCardListView(ListView):
    """Alternative Playercard Listview"""

    template_name = "djolowin/playercard/all_playercards.html"
    context_object_name = "playercards"
    paginate_by = settings.DJOLOWIN_PLAYERCARD_PAGINATE_BY

    def post(self, request, *args, **kwargs):
        form = PlayerCardFilterForm(request.POST)
        if form.is_valid():
            query = Q()
            playercards = list_of_cards_to_display()
            if form.cleaned_data.get("name"):
                query &= Q(player__name__icontains=form.cleaned_data["name"])
            if form.cleaned_data.get("team"):
                query &= Q(player__team__name__icontains=form.cleaned_data["team"])
            if form.cleaned_data.get("position"):
                query &= Q(player__position__icontains=form.cleaned_data["position"])
            if form.cleaned_data.get("rarity"):
                query &= Q(rarity__name__icontains=form.cleaned_data["rarity"])
            playercards = playercards.filter(query)
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
                "djolowin/playercard/all_playercards.html",
                {"playercards": playercards, "filter_form": form},
            )

    def get_queryset(self):
        # The method below is to only show playercards that are for sale and that are not from the MasterTeam COllection
        playercards = list_of_cards_to_display()
        return playercards

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = PlayerCardFilterForm(self.request.GET)
        context["filter"] = PlayerCardFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        context["teams"] = Team.objects.all()
        context["positions"] = Player.POSITION_CHOICES
        context["playercards"] = context["page_obj"]

        return context


class UserPlayerCardListView(ListView):
    model = PlayerCard
    context_object_name = "playercards"
    template_name = "djolowin/playercard/owned_playercard_list.html"
    paginate_by = settings.DJOLOWIN_PLAYERCARD_PAGINATE_BY

    def get_queryset(self):
        user = self.request.user
        queryset = PlayerCard.objects.filter(owner=user)

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(player__name__icontains=search)

        sort_by = self.request.GET.get("sort_by")
        order = self.request.GET.get("order")

        if sort_by:
            if order == "desc":
                sort_by = f"-{sort_by}"
            queryset = queryset.order_by(sort_by)

        return queryset


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
    user_wallet = UserWallet.objects.get(user=request.user)

    if user_wallet.balance >= playercard.price:
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
