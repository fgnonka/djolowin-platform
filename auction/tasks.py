# tasks.py
from celery import shared_task
from datetime import timedelta

from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail

from communication.notifications.actions import send_notification
from .models import Auction
from .auction_logic import (
    handle_auction_end,
    send_auction_ended_email,
    transfer_coins_to_seller,
)


@shared_task
def check_auction_end():
    all_auctions = Auction.objects.filter(auction_ended=False)
    for auction in all_auctions:
        if auction.has_ended:
            handle_auction_end(auction)
            transfer_coins_to_seller(auction)
            send_auction_ended_email(auction)
            auction.auction_ended = True
            auction.save()
            for user in auction.watchers.all():
                send_notification(
                    recipient=user,
                    subject=f"The {auction.rarity} auction of {auction.card.player.name} {auction.card.index} has ended!",
                    message=f"The auction for {auction.card.player.name} has ended.",
                )


@shared_task
def check_auction_ending_soon():
    all_auctions = Auction.objects.filter(auction_ended=False)
    for auction in all_auctions:
        card = auction.card
        if auction.is_ending_soon:
            message = render_to_string(
                "djolowin/auction/auction_end_notification.html",
                {"auction": auction, "card": card},
            )
            for user in auction.watchers.all():
                send_notification(
                    recipient=user,
                    subject=f"The {auction.rarity} auction of {auction.card.player.name} {auction.card.index} is ending soon!",
                    message=message,
                )
