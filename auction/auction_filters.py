from django import template

register = template.Library()

@register.filter
def get_auction_card_ids(auctions):
    """
    Returns a list of all card IDs for which an auction already exists.
    """
    return [auction.card.id for auction in auctions]
