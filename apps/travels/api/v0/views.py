from django.utils import translation
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.travels.api.v0.filters import TravelsFilter
from apps.travels.api.v0.serializers import (TravelListSerializer, TravelCreateSerializer,
                                             TravelUpdateSerializer, TravelCommentSerializer)
from apps.travels.models import Travel, TravelImage, TravelComments


class TravelListView(ListAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TravelsFilter

    @extend_schema(tags=["Travel"],
                   summary="Travellarning listini chiqarish")
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
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(tags=["Travel"],
                   summary="Travel create yaratish")
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

    @extend_schema(tags=["Travel"],
                   summary="Travel update to'liq yangilash")
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"detail": "Travel yangilandi"}, status=status.HTTP_200_OK)

    @extend_schema(tags=["Travel"],
                   summary="Travel update yangilash")
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
    serializer_class = TravelListSerializer
    lookup_field = 'pk'

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return Travel.objects.get(pk=pk)
        except Travel.DoesNotExist:
            raise NotFound(detail="Bunday Travel yo‘q", code=404)

    @extend_schema(tags=["Travel"],
                   summary="Travelni o'chirirsh",)
    def delete(self, request, *args, **kwargs):
        travel = self.get_object()
        travel.delete()
        return Response({"detail": f"{travel.title} sayohat joyi muvoffaqiyatli o‘chirildi"},
                        status=status.HTTP_200_OK)


class TravelDetailView(RetrieveAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelListSerializer
    lookup_field = 'pk'


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=["views"])
        return super().retrieve(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return Travel.objects.get(pk=pk)
        except Travel.DoesNotExist:
            raise NotFound(detail="Bunday Travel topilmadi.")

    @extend_schema(tags=["Travel"],summary="Travelning detailini chiqarish")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class TravelCommentCreateView(CreateAPIView):
    queryset = TravelComments.objects.all()
    serializer_class = TravelCommentSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]

    @extend_schema(tags=["Travel"], summary="Travel comment yaratish")
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class TravelCommentListView(ListAPIView):
    queryset = TravelComments.objects.all()
    serializer_class = TravelCommentSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        travel_id = self.kwargs.get("pk")
        return TravelComments.objects.filter(travel_id=travel_id).order_by("-created_at")

    @extend_schema(tags=["Travel"], summary="Travel comment listini kurish ")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


travel_delete_view = TravelDeleteView.as_view()
travel_update_view = TravelUpdateView.as_view()
travel_create_view = TravelCreateView.as_view()
travel_list_view = TravelListView.as_view()
travel_detail_view = TravelDetailView.as_view()
travel_comment_create = TravelCommentCreateView.as_view()
travel_comment_list = TravelCommentListView.as_view()


