from .models import Transaction

def create_card_purchase_transaction(user, card, amount_spent):
    transaction = Transaction.objects.create(
        user=user,
        transaction_type="card_purchase",
        card=card,
        amount_spent=amount_spent
    )
    return transaction

def create_bundle_purchase_transaction(user, bundle, amount_spent):
    transaction = Transaction.objects.create(
        user=user,
        transaction_type="bundle_purchase",
        bundle=bundle,
        amount_spent=amount_spent
    )
    return transaction

def create_currency_purchase_transaction(user, currency_package, amount_spent):
    transaction = Transaction.objects.create(
        user=user,
        transaction_type="currency_purchase",
        currency_package=currency_package,
        amount_spent=amount_spent
    )
    return transaction