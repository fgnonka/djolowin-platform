from .models import Transaction, InAppCurrencyTransaction, AuctionTransaction


def create_card_purchase_transaction(buyer, card, amount_spent, seller=None):
    if seller:
        transaction = Transaction.objects.create(
            buyer=buyer,
            seller=seller,
            transaction_type="card_purchase",
            card=card,
            amount_spent=amount_spent,
        )
    else:
        transaction = Transaction.objects.create(
            buyer=buyer,
            transaction_type="card_purchase",
            card=card,
            amount_spent=amount_spent,
        )
    return transaction


def create_bundle_purchase_transaction(buyer, bundle, amount_spent):
    transaction = Transaction.objects.create(
        buyer=buyer,
        transaction_type="bundle_purchase",
        bundle=bundle,
        amount_spent=amount_spent,
    )
    return transaction


def create_currency_purchase_transaction(
    user, currency_package, amount_spent, currency_amount
):
    transaction = InAppCurrencyTransaction.objects.create(
        user=user,
        currency_package=currency_package,
        amount_spent=amount_spent,
        currency_amount=currency_amount,
    )
    return transaction


def create_auction_transaction(
    seller,
    winner,
    auction,
    start_price,
    winning_bid,
    start_time,
    end_time,
    number_of_bids,
    number_of_watchers,
):
    transaction = AuctionTransaction.objects.create(
        seller=seller,
        winner=winner,
        auction=auction,
        start_price=start_price,
        winning_bid=winning_bid,
        start_time=start_time,
        end_time=end_time,
        number_of_bids=number_of_bids,
        number_of_watchers=number_of_watchers,
    )
    return transaction
