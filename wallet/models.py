from django.db import models
from django.utils.translation import gettext_lazy as _


class UserWallet(models.Model):
    user = models.OneToOneField('account.CustomUser', on_delete=models.CASCADE, related_name='wallet')
    balance = models.PositiveIntegerField(default=0)
    reserved_balance = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def available_balance(self):
        return self.balance - self.reserved_balance

    def __str__(self):
        return f"{self.user} - {self.balance}"

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")