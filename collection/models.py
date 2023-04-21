from django.conf import settings
from django.db import models
from django.urls import reverse


from base.models import Team



User = settings.AUTH_USER_MODEL

class Collection(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    cards = models.ManyToManyField('playercard.PlayerCard')
    reward = models.PositiveIntegerField(help_text="Reward in DJOBA coins", default=100000)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('collection:detail', kwargs={'pk': self.pk})
    
    def get_cards(self):
        return self.cards.all()