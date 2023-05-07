from django.contrib import admin
from .models import Transaction, InAppCurrencyTransaction, AuctionTransaction
# Register your models here.

admin.site.register(AuctionTransaction)
admin.site.register(Transaction)
admin.site.register(InAppCurrencyTransaction)