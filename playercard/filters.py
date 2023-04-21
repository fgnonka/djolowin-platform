import django_filters
from .models import PlayerCard

class PlayerCardFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='player__name', lookup_expr='icontains')
    position = django_filters.CharFilter(field_name='player__position', lookup_expr='exact')
    team__name = django_filters.CharFilter(field_name='player__team__name', lookup_expr='icontains')
    
    class Meta:
        model = PlayerCard
        fields = ['name', 'position', 'team__name']
