from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status
from django.utils import translation
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.restaurants.api.v0.filters import RestaurantsFilter
from .serializers import (RestaurantCreateSerializer, RestaurantSerializer,
                          RestaurantUpdateSerializer, RestaurantCommentSerializer)
from apps.restaurants.models import Restaurant, RestaurantComments
from rest_framework.generics import (ListAPIView, CreateAPIView, UpdateAPIView,
                                     DestroyAPIView, RetrieveAPIView)





class RestaurantListView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RestaurantsFilter
    search_fields = ['title', 'description']

    @extend_schema(tags=["Restaurant"],
                   summary="Restaurant listini chiqarish")
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

    @extend_schema(tags=["Restaurant"], summary="Restaurant create qilish")
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        restaurant = serializer.save()


        read_serializer = RestaurantSerializer(restaurant, context=self.get_serializer_context())
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


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

    @extend_schema(tags=["Restaurant"],
                   summary="Restaurant to'liq update qilish")
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "detail": "Restoran ma'lumotlari to‘liq yangilandi",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @extend_schema(tags=["Restaurant"],
                   summary="Restaurant update qilish")
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
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            raise NotFound(detail="Bunday restoran topilmadi.")

    @extend_schema(tags=["Restaurant"],
                   summary="Restaurant delete qilish")
    def delete(self, request, *args, **kwargs):
        restaurant = self.get_object()
        restaurant.delete()
        return Response(
            {"detail": f"{restaurant.name_uz} restorani muvaffaqiyatli o‘chirildi."},
            status=status.HTTP_200_OK
        )


class RestaurantDetailView(RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'pk'


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=["views"])
        return super().retrieve(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            raise NotFound(detail="Bunday restoran topilmadi.")

    @extend_schema(tags=["Restaurant"], summary="Restaurant ma'lumotlarini ko'rish")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RestaurantCommentCreateView(CreateAPIView):
    queryset = RestaurantComments.objects.all()
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = RestaurantCommentSerializer

    @extend_schema(tags=["Restaurant"], summary="Create restaurant comment")
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class RestaurantCommentListView(ListAPIView):
    queryset = RestaurantComments.objects.all()
    serializer_class = RestaurantCommentSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'pk'

    def get_queryset(self):
        restaurant = self.kwargs['pk']
        return RestaurantComments.objects.filter(restaurant_id=restaurant).order_by('-created_at')


    @extend_schema(tags=["Restaurant"], summary="List Restaurant comment")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)





resraurant_comment_list_view = RestaurantCommentListView.as_view()
restaurant_comment_create_view = RestaurantCommentCreateView.as_view()
restaurant_detail_view = RestaurantDetailView.as_view()
restaurant_delete_view = RestaurantDeleteView.as_view()
restaurant_update_view = RestaurantUpdateView.as_view()
restaurant_create_view = RestaurantCreateView.as_view()
resturant_list = RestaurantListView.as_view()

