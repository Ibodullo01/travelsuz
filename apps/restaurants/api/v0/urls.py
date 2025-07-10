from django.urls import path

from .views import (resturant_list, restaurant_create_view, restaurant_detail_view,
                    restaurant_update_view, restaurant_delete_view, restaurant_comment_create_view,
                    resraurant_comment_list_view)

app_name = 'restaurants_api'

urlpatterns = [
    path('restaurants/', resturant_list, name='restaurants_list'),
    path('restaurant_create/', restaurant_create_view, name='restaurant_create'),
    path('restaurant_update/<int:pk>/', restaurant_update_view, name='restaurant_update'),
    path('restaurant_delete/<int:pk>/', restaurant_delete_view, name='restaurant_delete'),
    path('restaurant_detail/<int:pk>/', restaurant_detail_view, name='restaurant_detail'),
    path('restaurant_coment_create/', restaurant_comment_create_view, name='restaurant_comment_create'),
    path('restaurant_comment_list/<int:pk>/', resraurant_comment_list_view, name='restaurant_comment_list'),
]