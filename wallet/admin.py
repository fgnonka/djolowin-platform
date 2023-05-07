from django.contrib import admin
from .models import UserWallet
# Register your models here.
class UserWalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "reserved_balance")
    list_filter = ("user",)
    search_fields = ("user",)
    ordering = ("user",)


admin.site.register(UserWallet, UserWalletAdmin)