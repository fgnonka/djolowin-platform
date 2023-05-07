from django.core.mail import send_mail
from django.conf import settings

from .signals import completed_auction

def handle_auction_end(auction):
    """This function is called when an auction ends.
    It checks if there are any bids on the auction
    and if there are, it transfers the card to the highest bidder.
    If there are no bids, the card is returned to the auction owner.
    Args:
        auction: The auction that has ended.
    """
    highest_bid = auction.get_highest_bid()
    if highest_bid:
        auction.card.owner = highest_bid.bidder
        auction.card.save()
    else:
        auction.card.owner = auction.owner
        auction.card.save()


def transfer_coins_to_seller(auction):
    """This function is called when an auction ends.
    It checks if there are any bids on the auction
    and if there are, it transfers the coins to the auction owner.
    Args:
        auction: The auction that has ended.
    """
    highest_bid = auction.get_highest_bid()
    if highest_bid:
        highest_bidder_wallet = highest_bid.bidder.wallet
        highest_bidder_wallet.reserved_balance -= highest_bid.amount
        highest_bidder_wallet.balance -= highest_bid.amount
        highest_bidder_wallet.save()
        owner_wallet = auction.owner.wallet
        owner_wallet.balance += highest_bid.amount
        auction.owner.wallet.save()


def send_auction_ended_email(auction):
    """This function is called when an auction ends.
    It sends an email to all users watching the auction.
    Args:
        auction: The auction that has ended.
    """
    highest_bid = auction.bid_set.order_by("-amount").first()
    for user in auction.watchers.all():
        send_mail(
            "Auction Ended",
            f"The auction for {auction.card} has ended.",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

    if highest_bid:
        # Send email to winner
        send_mail(
            "Auction Won",
            f"You won the auction for {auction.card} for {highest_bid.amount} DJOBA.",
            settings.DEFAULT_FROM_EMAIL,
            [highest_bid.bidder.email],
            fail_silently=False,
        )
        # Send email to auction owner
        send_mail(
            "Auction Ended",
            f"The auction for {auction.card} has ended. You sold it to {highest_bid.bidder} for ${highest_bid.amount}.",
            settings.DEFAULT_FROM_EMAIL,
            [auction.owner.email],
            fail_silently=False,
        )
