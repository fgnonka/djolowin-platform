from django.db import models
from django.urls import reverse
from collection.models import Collection

class DJOBAReward(models.Model):    
    name = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.PositiveIntegerField(help_text="Reward in DJOBA coins", default=500000)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.amount} DJOBA'

    def get_absolute_url(self):
        return reverse('reward:detail', kwargs={'pk': self.pk})
