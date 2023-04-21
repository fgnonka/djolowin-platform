# tasks.py
from celery import shared_task
from datetime import timedelta

from django.db.models import Q
from django.core.mail import send_mail

from .models import Auction, Bid
from .auction_logic import handle_auction_end

@shared_task
def send_auction_ending_soon_notifications():
    auctions_ending_soon = Auction.objects.filter(ending_soon=True)

    for auction in auctions_ending_soon:
        for user in auction.watchers.all():
            send_mail(
                "Auction Ending Soon",
                f"The auction for {auction.card.name} is ending in an hour.",
                "noreply@example.com",
                [user.email],
                fail_silently=False,
            )


@shared_task
def send_outbid_notification(bid_id):
    bid = Bid.objects.get(id=bid_id)
    auction = bid.auction
    current_bidder = bid.bidder

    # Get the previous highest bid
    previous_highest_bid = (
        Bid.objects.filter(Q(auction=auction) & ~Q(bidder=current_bidder))
        .order_by("-amount")
        .first()
    )

    if previous_highest_bid:
        outbid_user = previous_highest_bid.bidder
        send_mail(
            "You have been outbid",
            f"Your bid for {auction.card} has been outbid by another user. The new highest bid is {bid.amount}.",
            "noreply@example.com",
            [outbid_user.email],
            fail_silently=False,
        )


@shared_task
def check_auction_end():
    ended_auctions = Auction.objects.filter(has_ended=True)
    for auction in ended_auctions:
        handle_auction_end(auction)
        auction.save()