import django_filters
from .models import PlayerCard
from base.models import Player

class PlayerCardFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='player__name', lookup_expr='icontains')
    position = django_filters.ChoiceFilter(choices=Player.POSITION_CHOICES)
    team = django_filters.CharFilter(field_name='player__team__name', lookup_expr='in')


    class Meta:
        model = PlayerCard
        fields = ['name', 'position', 'team']
