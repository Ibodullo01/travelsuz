from modeltranslation.utils import get_language
from rest_framework import serializers

from apps.hotels.models import Regions
from apps.travels.models import Travel


class TravelListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    place_type = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()

    class Meta:
        model = Travel
        fields = [
            'id',
            'title', 'description', 'address', 'place_type',
            'ticket_price',
            'image',
            'location_url',
            'region',
            'created_at',
        ]

    def get_lang(self):
        return get_language() or 'uz'

    def get_title(self, obj):
        return getattr(obj, f"title_{self.get_lang()}", obj.title_uz)

    def get_description(self, obj):
        return getattr(obj, f"description_{self.get_lang()}", obj.description_uz)

    def get_address(self, obj):
        return getattr(obj, f"address_{self.get_lang()}", obj.address_uz)

    def get_place_type(self, obj):
        return getattr(obj, f"place_type_{self.get_lang()}", obj.place_type_uz)

    def get_region(self, obj):
        return getattr(obj.region, f"name_{self.get_lang()}", obj.region.name)



class TravelCreateSerializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(
        queryset=Regions.objects.all(),
        required=False
    )
    class Meta:
        model = Travel
        fields = [
            'title', 'title_uz', 'title_ru', 'title_en',
            'description', 'description_uz', 'description_ru', 'description_en',
            'address', 'address_uz', 'address_ru', 'address_en',
            'place_type', 'place_type_uz', 'place_type_ru', 'place_type_en',
            'ticket_price',
            'image',
            'location_url',
            'region',
            'created_at',]


class TravelUpdateSerializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(
        queryset=Regions.objects.all(),
        required=False
    )
    class Meta:
        model = Travel
        fields = [
            'id',
            'title', 'title_uz', 'title_ru', 'title_en',
            'description', 'description_uz', 'description_ru', 'description_en',
            'address', 'address_uz', 'address_ru', 'address_en',
            'place_type', 'place_type_uz', 'place_type_ru', 'place_type_en',
            'ticket_price',
            'image',
            'location_url',
            'region',
            'created_at', ]





