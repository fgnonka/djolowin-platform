from django.contrib import admin

# Register your models here.
from .models import Auction, Bid


class AuctionAdmin(admin.ModelAdmin):
    list_display = (
        "card",
        "owner",
        "starting_price",
        "current_bid",
        "highest_bidder",
        "start_time",
        "end_time",
        "is_active",
    )
    list_filter = ("owner", "highest_bidder")
    search_fields = ("card", "owner", "highest_bidder")
    date_hierarchy = "start_time"
    ordering = ("-start_time",)


class BidAdmin(admin.ModelAdmin):
    list_display = ("auction", "bidder", "amount", "timestamp")
    list_filter = ("auction", "bidder")
    search_fields = ("auction", "bidder")
    date_hierarchy = "timestamp"
    ordering = ("-timestamp",)


admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
