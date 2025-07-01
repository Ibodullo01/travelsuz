from django.utils import translation
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

    def get_queryset(self):
        # lang= query parametri asosida tilni aktivlashtirish

        lang = self.request.query_params.get('lang', 'uz')
        if lang not in ['uz', 'ru', 'en']:
            lang = 'uz'
        translation.activate(lang)

        # region= query parametri asosida filter

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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"detail": "Muvoffaqiyatli yangilandi"}, status=status.HTTP_200_OK)

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Muvoffaqiyatli o‘chirildi"}, status=status.HTTP_200_OK)




travel_delete_view = TravelDeleteView.as_view()
travel_update_view = TravelUpdateView.as_view()
travel_create_view = TravelCreateView.as_view()
travel_list_view = TravelListView.as_view()