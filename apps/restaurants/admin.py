from django.contrib import admin

from apps.restaurants.models import Restaurant, RestaurantComments,RestaurantImage

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(RestaurantComments)
admin.site.register(RestaurantImage)