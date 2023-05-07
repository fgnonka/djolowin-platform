# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from .models import Bid


completed_auction = Signal()

