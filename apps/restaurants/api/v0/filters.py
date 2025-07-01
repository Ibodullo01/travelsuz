import django_filters
from apps.restaurants.models import Restaurant

class RestaurantsFilter(django_filters.FilterSet):
    region = django_filters.NumberFilter(field_name='region__id')

    class Meta:
        model = Restaurant
        fields = ['region']
