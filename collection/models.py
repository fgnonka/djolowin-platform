from django.conf import settings
from django.db import models
from django.urls import reverse


from base.models import Team
from playercard.models import CardRarity



User = settings.AUTH_USER_MODEL

class Collection(models.Model):
    name=models.CharField(max_length=100)
    rarity = models.ForeignKey('playercard.CardRarity', on_delete=models.CASCADE, blank=True, null=True)
    description=models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    cards = models.ManyToManyField('playercard.PlayerCard', related_name='collections')
    reward = models.ForeignKey('reward.DJOBAReward', on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('collection:detail', kwargs={'pk': self.pk})
    
    def get_cards(self):
        return self.cards.all()
    
    
class CompletedCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    reward = models.ForeignKey('reward.DJOBAReward', on_delete=models.CASCADE, blank=True, null=True)
    reward_received = models.BooleanField(default=False)
    date_completed = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user} - {self.collection}'
    
    class Meta:
        unique_together = ('user', 'collection')