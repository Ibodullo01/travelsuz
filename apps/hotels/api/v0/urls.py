from django.urls import path
from .views import (hotels_views, hotel_detail_view,
                    hotel_create_view, regions_views,
                    regions_create_view, hotel_update_view,
                    hotel_delete_view, regions_update_view,
                    regions_delete_view)

app_name = 'hotels_api'
urlpatterns = [
    path('hotel_list/', hotels_views, name='hotels_views' ),
    path( 'hotel_detail/<int:pk>/', hotel_detail_view, name='hotel_detail_view' ),
    path('hotel_create/', hotel_create_view, name='hotel_create_view' ),
    path('regions_list/', regions_views, name='regions_views' ),
    path('region_create/', regions_create_view, name='regions_create_view' ),
    path('hotel_update/<int:pk>', hotel_update_view, name='hotel_update_view' ),
    path('hotel_delete/<int:pk>', hotel_delete_view, name='hotel_delete_view'),
    path('region_update/<int:pk>', regions_update_view, name='region_update_view' ),
    path('region_delete/<int:pk>', regions_delete_view, name='region_delete_view'),

]
