import django_filters
from apps.hotels.models import Hotel

class HotelFilter(django_filters.FilterSet):
    region = django_filters.NumberFilter(field_name='region__id')

    class Meta:
        model = Hotel
        fields = ['region']
