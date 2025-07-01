from http import HTTPStatus

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from apps.hotels.models import Regions, Hotel
from .filters import HotelFilter
from .serializers import (HotelSerializer, HotelCreateSerializer,
                          RegionSerializer, RegionCreateSerializer,
                          HotelUpdateSerializer)


from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from django.utils import translation


class HotelListAPIView(ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelFilter

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='region',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Region ID bo‘yicha filter'
            ),
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Tilni belgilang: uz, ru, en'
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        lang = request.query_params.get('lang')
        if lang in ['uz', 'ru', 'en']:
            with translation.override(lang):
                return super().get(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

class HotelDetailView(RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    lookup_field = 'pk'

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return Hotel.objects.get(pk=pk)
        except Hotel.DoesNotExist:
            raise NotFound(detail="Bunday Hotel topilmadi.")



class HotelCreateView(CreateAPIView):
    queryset = Hotel.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    serializer_class = HotelCreateSerializer
    parser_classes = [MultiPartParser, FormParser]

class HotelUpdateView(UpdateAPIView):
    queryset = Hotel.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    serializer_class = HotelUpdateSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'pk'

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            region = Regions.objects.get(pk=pk)
        except Regions.DoesNotExist:
            raise NotFound(detail="Bunday region topilmadi.")

        if not self.request.user.is_staff:
            raise PermissionDenied("Sizda bu amalni bajarish huquqi yo‘q.")

        return region

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()  # Bu yerda yuqoridagi ruxsat va mavjudlik tekshiriladi
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "detail": "Region ma'lumotlari muvaffaqiyatli yangilandi",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class HotelDeleteView(DestroyAPIView):
    queryset = Hotel.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'pk'

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return Hotel.objects.get(pk=pk)
        except Hotel.DoesNotExist:
            raise NotFound(detail="Bunday Hotel topilmadi.")

    def delete(self, request, pk):
        hotel = Hotel.objects.get(pk=pk)
        if not request.user.is_authenticated:
            return Response({'detail': f'Siz bu {hotel.title} ni uchira olmaysiz '},
                     status=status.HTTP_401_UNAUTHORIZED)
        else:
            hotel.delete()
            return Response({"detail": f"{hotel.title} o‘chirildi."},
                        status=status.HTTP_200_OK)

class RegionUpdateView(UpdateAPIView):
    queryset = Regions.objects.all().order_by('id')
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated,]
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'pk'

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            region = Regions.objects.get(pk=pk)
        except Regions.DoesNotExist:
            raise NotFound(detail="Bunday region topilmadi.")


        if not self.request.user.is_authenticated:
            raise PermissionDenied("Sizda bu amalni bajarish huquqi yo‘q.")

        return region

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()  # Bu yerda yuqoridagi ruxsat va mavjudlik tekshiriladi
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "detail": "Region ma'lumotlari muvaffaqiyatli yangilandi",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class RegionsListView(ListAPIView):
    queryset = Regions.objects.all()
    serializer_class = RegionSerializer

    def get(self, request):
        lang = request.query_params.get('lang')
        if lang:
            translation.activate(lang)

        queryset = Regions.objects.all()
        serializer = RegionSerializer(queryset, many=True)
        return Response(serializer.data)


class RegionCreateView(CreateAPIView):
    queryset = Regions.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    serializer_class = RegionCreateSerializer
    parser_classes = (MultiPartParser, FormParser)


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RegionDeleteView(DestroyAPIView):
    queryset = Regions.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        region = Regions.objects.get(pk=pk)

        if not request.user.is_authenticated:
            return Response({"detail": f"Siz bu {region.name} o‘chira olmaysiz."},
                            status=status.HTTP_403_FORBIDDEN)
        region.delete()
        return Response({"detail": f"{region.name} o‘chirildi."},
                        status=status.HTTP_200_OK)




hotel_delete_view = HotelDeleteView.as_view()
hotel_create_view = HotelCreateView.as_view()
hotel_detail_view = HotelDetailView.as_view()
hotels_views = HotelListAPIView.as_view()
hotel_update_view = HotelUpdateView.as_view()
regions_views = RegionsListView.as_view()
regions_create_view = RegionCreateView.as_view()
regions_update_view = RegionUpdateView.as_view()
regions_delete_view = RegionDeleteView.as_view()
