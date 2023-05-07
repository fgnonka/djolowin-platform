# tasks.py
from celery import shared_task
from datetime import timedelta

from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail

from .models import Auction, Bid
from .auction_logic import handle_auction_end, send_auction_ended_email, transfer_coins_to_seller



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
        

@shared_task
def check_auction_ending_soon():
    all_auctions = Auction.objects.filter(auction_ended=False)
    for auction in all_auctions:
        if auction.is_ending_soon:
            send_mail(
                "Auction Ending Soon",
                f"The auction for {auction.card} is ending in less than 1hour.",
                settings.DEFAULT_FROM_EMAIL,
                [user.email for user in auction.watchers.all()],
                fail_silently=False,
            )