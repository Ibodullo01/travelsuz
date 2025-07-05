from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from django.utils import translation
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

from apps.restaurants.api.v0.filters import RestaurantsFilter
from .serializers import (RestaurantCreateSerializer, RestaurantSerializer,
                          RestaurantUpdateSerializer)
from apps.restaurants.models import Restaurant
from rest_framework.generics import (ListAPIView, CreateAPIView, UpdateAPIView,
                                     DestroyAPIView)


language_param = openapi.Parameter(
    name='Accept-Language',
    in_=openapi.IN_HEADER,
    description='Language: uz, ru, en',
    type=openapi.TYPE_STRING,
    required=False,
    default='uz'
)


class RestaurantListView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RestaurantsFilter
    search_fields = ['title', 'description']

    @swagger_auto_schema(tags=["Restaurant"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        lang = self.request.query_params.get('lang', 'uz')
        if lang not in ['uz', 'ru', 'en']:
            lang = 'uz'
        translation.activate(lang)
        return Restaurant.objects.all()


class RestaurantCreateView(CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantCreateSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Restaurant"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RestaurantUpdateView(UpdateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'pk'

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            raise NotFound(detail="Bunday restoran topilmadi.", code=404)

    @swagger_auto_schema(tags=["Restaurant"])
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "detail": "Restoran ma'lumotlari to‘liq yangilandi",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Restaurant"])
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "detail": "Restoran ma'lumotlari qisman yangilandi",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class RestaurantDeleteView(DestroyAPIView):
    queryset = Restaurant.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'pk'

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            raise NotFound(detail="Bunday restoran topilmadi.")

    @swagger_auto_schema(tags=["Restaurant"])
    def delete(self, request, *args, **kwargs):
        restaurant = self.get_object()

        if not request.user.is_authenticated:
            return Response(
                {"detail": f"Siz bu {restaurant.name_uz} restoranini o‘chira olmaysiz."},
                status=status.HTTP_403_FORBIDDEN
            )

        restaurant.delete()
        return Response(
            {"detail": f"{restaurant.name_uz} restorani muvaffaqiyatli o‘chirildi."},
            status=status.HTTP_200_OK
        )
restaurant_delete_view = RestaurantDeleteView.as_view()
restaurant_update_view = RestaurantUpdateView.as_view()
restaurant_create_view = RestaurantCreateView.as_view()
resturant_list = RestaurantListView.as_view()

