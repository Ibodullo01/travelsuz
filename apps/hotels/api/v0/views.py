from typing import Any

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.hotels.models import Regions, Hotel, HotelComment
from .filters import HotelFilter
from .serializers import (HotelSerializer, HotelCreateSerializer,
                          RegionSerializer, RegionCreateSerializer,
                          HotelUpdateSerializer, HotelCommentSerializer)

from django.utils import translation


class HotelListAPIView(ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelFilter

    @extend_schema(tags=["Hotels"], summary="Hotellarni listini ko'rish")
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=["views"])
        return super().retrieve(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return Hotel.objects.get(pk=pk)
        except Hotel.DoesNotExist:
            raise NotFound(detail="Bunday Hotel topilmadi.")

    @extend_schema(tags=["Hotels"], summary="Hotel ma'lumotlarini ko'rish")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



class HotelCreateView(CreateAPIView):
    queryset = Hotel.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    serializer_class = HotelCreateSerializer
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(tags=["Hotels"], summary="Hotel create yaratish")
    def post(self, request, *args: Any, **kwargs: Any) -> Response:
        return super().post(request, *args, **kwargs)


class HotelUpdateView(UpdateAPIView):
    queryset = Hotel.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    serializer_class = HotelUpdateSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'pk'

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            hotel = Hotel.objects.get(pk=pk)
            return hotel
        except Hotel.DoesNotExist:
            raise NotFound(detail="Bunday hotel topilmadi.")


    @extend_schema(tags=["Hotels"], summary="Hotel update qilish ")
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "detail": "Hotel ma'lumotlari to‘liq yangilandi",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @extend_schema(tags=["Hotels"], summary="Hotelni qisman update qilish")
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "detail": "Hotel ma'lumotlari qisman yangilandi",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class HotelDeleteView(DestroyAPIView):
    queryset = Hotel.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = HotelSerializer
    lookup_field = 'pk'


    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return Hotel.objects.get(pk=pk)
        except Hotel.DoesNotExist:
            raise NotFound(detail="Bunday Hotel topilmadi.")

    @extend_schema(tags=["Hotels"], summary="Hotelni o'chirish")
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
    permission_classes = [IsAuthenticated]
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

    @extend_schema(tags=["Region"] , summary="Region Update qilish")
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "detail": "Region ma'lumotlari to‘liq yangilandi",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @extend_schema(tags=["Region"], summary="Region qisman Update qilish")
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "detail": "Region ma'lumotlari qisman yangilandi",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class RegionsListView(ListAPIView):
    queryset = Regions.objects.all()
    serializer_class = RegionSerializer

    @extend_schema(tags=["Region"], summary="Barcha regionlar listini chiqarish")
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

    @extend_schema(tags=["Region"], summary="Create region ")
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RegionDeleteView(DestroyAPIView):
    queryset = Regions.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    serializer_class = RegionSerializer

    @extend_schema(tags=["Region"], summary="Region Delete qilish")
    def delete(self, request, pk):
        region = Regions.objects.get(pk=pk)

        if not request.user.is_authenticated:
            return Response({"detail": f"Siz bu {region.name} o‘chira olmaysiz."},
                            status=status.HTTP_403_FORBIDDEN)
        region.delete()
        return Response({"detail": f"{region.name} o‘chirildi."},
                        status=status.HTTP_200_OK)

class HotelCommentCreateView(CreateAPIView):
    queryset = HotelComment.objects.all()
    serializer_class = HotelCommentSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(tags=["Hotels"], summary="Create hotel comment")
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)




class HotelCommentListView(ListAPIView):
    queryset = HotelComment.objects.all()
    serializer_class = HotelCommentSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'


    def get_queryset(self):
        hotel_id = self.kwargs['pk']
        return HotelComment.objects.filter(hotel_id=hotel_id).order_by('-created_at')


    @extend_schema(tags=["Hotels"], summary="List hotel comment")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



hotel_comment_list_view = HotelCommentListView.as_view()
hotel_comment_create_view = HotelCommentCreateView.as_view()
hotel_delete_view = HotelDeleteView.as_view()
hotel_create_view = HotelCreateView.as_view()
hotel_detail_view = HotelDetailView.as_view()
hotels_views = HotelListAPIView.as_view()
hotel_update_view = HotelUpdateView.as_view()
regions_views = RegionsListView.as_view()
regions_create_view = RegionCreateView.as_view()
regions_update_view = RegionUpdateView.as_view()
regions_delete_view = RegionDeleteView.as_view()
