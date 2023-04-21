import django.dispatch

playercard_viewed = django.dispatch.Signal()

trade_initiated = django.dispatch.Signal()
auction_initiated = django.dispatch.Signal()

completed_trade = django.dispatch.Signal()
completed_auction = django.dispatch.Signal()
completed_purchase = django.dispatch.Signal()
