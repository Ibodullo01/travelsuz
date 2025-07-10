from django.urls import path
from .views import (travel_list_view, travel_create_view, travel_detail_view,
                    travel_update_view, travel_delete_view, travel_comment_create, travel_comment_list)

app_name = 'travels_api'

urlpatterns = [

    path('travel_list/', travel_list_view, name='travel_list'),
    path('travel_create/', travel_create_view, name='travel_create'),
    path('travel_update/<int:pk>/', travel_update_view, name='travel_update'),
    path('travel_delete/<int:pk>/', travel_delete_view, name='travel_delete'),
    path('travel_detail/<int:pk>/', travel_detail_view, name='travel_detail'),
    path('travel_comment_create/', travel_comment_create, name='travel_comment_create'),
    path('travel_comment_list/<int:pk>/', travel_comment_list, name='travel_comment_list'),
]