from django.urls import path
from .views import (travel_list_view, travel_create_view,
                    travel_update_view, travel_delete_view)

app_name = 'restaurants_api'

urlpatterns = [

    path('travel_list/', travel_list_view, name='travel_list'),
    path('travel_create/', travel_create_view, name='travel_create'),
    path('travel_update/<int:pk>', travel_update_view, name='travel_update'),
    path('travel_delete/<int:pk>', travel_delete_view, name='travel_delete'),
]