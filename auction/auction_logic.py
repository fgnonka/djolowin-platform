#
def handle_auction_end(auction):
    """This function is called when an auction ends. 
    It checks if there are any bids on the auction 
    and if there are, it transfers the card to the highest bidder. 
    If there are no bids, the card is returned to the auction owner.
    Args:
        auction: The auction that has ended.
    """
    highest_bid = auction.bid_set.order_by("-amount").first()
    if highest_bid:
        auction.card.owner = highest_bid.bidder
        auction.card.save()
    else:
        auction.card.owner = auction.owner
        auction.card.save()
