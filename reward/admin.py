from django import forms
from django.contrib import admin

from .models import DJOBAReward
from playercard.models import PlayerCard

# admin.site.register(Reward)

class DJOBARewardAdmin(admin.ModelAdmin):
    model = DJOBAReward
    list_display = ('name', 'description', 'amount', 'is_active')
    list_editable = ('is_active','amount')
    list_filter = ('is_active','amount')
    search_fields = ('name', 'description')

admin.site.register(DJOBAReward, DJOBARewardAdmin)

