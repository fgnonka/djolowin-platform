from django.utils import timezone
from django.db.models import Q

from .models import Auction
from transaction.models import AuctionTransaction

def add_watcher(user,auction):
    auction_transcation = AuctionTransaction.objects.get(auction=auction)
    watchers_list = auction.watchers.all()
    if user not in watchers_list:
        auction.watchers.add(user)
        auction_transcation.number_of_watchers += 1
        auction.save()
    auction_transcation.save()
    
def remove_watcher(user,auction):
    auction_transcation = AuctionTransaction.objects.get(auction=auction)
    watchers_list = auction.watchers.all()
    if user in watchers_list:
        auction.watchers.remove(user)
        auction_transcation.number_of_watchers -= 1
        auction.save()
    auction_transcation.save()
    
def increase_number_of_bids(auction):
    auction_transcation = AuctionTransaction.objects.get(auction=auction)
    auction_transcation.number_of_bids += 1
    auction_transcation.save()


def has_existing_active_auction(card, owner):
    """ Check if the user has an active auction for the card."""
    existing_active_auction = Auction.objects.filter(
        Q(card=card) & Q(owner=owner) & Q(auction_ended=False) 
    )
    if existing_active_auction:
        #if the user has an active auction for the card
        return True
    return False
    
