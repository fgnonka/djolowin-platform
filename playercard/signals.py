import django.dispatch

playercard_viewed = django.dispatch.Signal()

trade_initiated = django.dispatch.Signal()
auction_initiated = django.dispatch.Signal()

completed_bundle_purchase = django.dispatch.Signal()
completed_card_purchase = django.dispatch.Signal()
