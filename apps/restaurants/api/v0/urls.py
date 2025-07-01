from django.urls import path

from .views import (resturant_list, restaurant_create_view,
                    restaurant_update_view, restaurant_delete_view)

app_name = 'restaurants_api'

urlpatterns = [
    path('restaurants/', resturant_list, name='restaurants_list'),
    path('restaurant_create/', restaurant_create_view, name='restaurant_create'),
    path('restaurant_update/<int:pk>', restaurant_update_view, name='restaurant_update'),
    path('restaurant_delete/<int:pk>', restaurant_delete_view, name='restaurant_delete'),
]