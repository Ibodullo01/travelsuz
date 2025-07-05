from django.utils import translation
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.travels.api.v0.serializers import (TravelListSerializer, TravelCreateSerializer,
                                             TravelUpdateSerializer)
from apps.travels.models import Travel



class TravelListView(ListAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelListSerializer

    @swagger_auto_schema(tags=["Travel"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        lang = self.request.query_params.get('lang', 'uz')
        if lang not in ['uz', 'ru', 'en']:
            lang = 'uz'
        translation.activate(lang)

        queryset = Travel.objects.all()
        region_id = self.request.query_params.get('region')
        if region_id:
            queryset = queryset.filter(region_id=region_id)
        return queryset


class TravelCreateView(CreateAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelCreateSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Travel"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TravelUpdateView(UpdateAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelUpdateSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return Travel.objects.get(pk=pk)
        except Travel.DoesNotExist:
            raise NotFound(detail="Bunday Travel yo‘q", code=404)

    @swagger_auto_schema(tags=["Travel"])
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"detail": "To‘liq yangilandi"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Travel"])
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"detail": "Qisman yangilandi"}, status=status.HTTP_200_OK)


class TravelDeleteView(DestroyAPIView):
    queryset = Travel.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'pk'

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return Travel.objects.get(pk=pk)
        except Travel.DoesNotExist:
            raise NotFound(detail="Bunday Travel yo‘q", code=404)

    @swagger_auto_schema(tags=["Travel"])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Muvoffaqiyatli o‘chirildi"}, status=status.HTTP_200_OK)

travel_delete_view = TravelDeleteView.as_view()
travel_update_view = TravelUpdateView.as_view()
travel_create_view = TravelCreateView.as_view()
travel_list_view = TravelListView.as_view()