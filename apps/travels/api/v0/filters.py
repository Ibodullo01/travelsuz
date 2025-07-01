import django_filters
from apps.travels.models import Travel

class TravelsFilter(django_filters.FilterSet):
    region = django_filters.NumberFilter(field_name='region__id')

    class Meta:
        model = Travel
        fields = ['region']
