from typing import List, Dict, Optional, Any

from drf_spectacular.utils import extend_schema_field
from modeltranslation.utils import get_language
from rest_framework import serializers
import json
from apps.hotels.models import Regions
from apps.travels.models import Travel, TravelImage, TravelComments


class TravelListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = Travel
        fields = [
            'id',
            'title', 'description', 'address',
            'region',
            'images',
            'location',
            'created_at',
            'views'
        ]

    def get_lang(self) -> str:
        return get_language() or 'uz'

    def get_title(self, obj) -> str:
        return getattr(obj, f"title_{self.get_lang()}", None)

    def get_description(self, obj) -> str:
        return getattr(obj, f"description_{self.get_lang()}", None)

    def get_address(self, obj) -> str:
        return getattr(obj, f"address_{self.get_lang()}", None)

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_images(self, obj) -> List[str]:
        return [img.image.url for img in obj.images.all()]

    @extend_schema_field(
        serializers.DictField(
            child=serializers.FloatField(allow_null=True),
            help_text="Location as { latitude, longitude }"
        )
    )
    def get_location(self, obj) -> Dict[str, Optional[float]]:
        loc = obj.location or {}
        return {
            "latitude": loc.get("latitude", None),
            "longitude": loc.get("longitude", None)
        }

    @extend_schema_field(serializers.CharField())
    def get_region(self, obj) -> str:
        lang = get_language()
        return getattr(obj.region, f'name_{lang}', obj.region.name)


class TravelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelImage
        fields = ['id', 'image']


class TravelCreateSerializer(serializers.ModelSerializer):

    title_uz = serializers.CharField(default="", help_text="Title uz ni kiriting")
    title_ru = serializers.CharField(default="", help_text="Title ru ni kiriting")
    title_en = serializers.CharField(default="", help_text="Title en ni kiriting")

    description_uz = serializers.CharField(default="", help_text="Description uz ni kiriting")
    description_ru = serializers.CharField(default="", help_text="Description ru ni kiriting")
    description_en = serializers.CharField(default="", help_text="Description en ni kiriting")

    address_uz = serializers.CharField(default="", help_text="Address uz ni kiriting")
    address_ru = serializers.CharField(default="", help_text="Adress ru ni kiriting")
    address_en = serializers.CharField(default="", help_text="Adress en ni kiriting")


    latitude = serializers.FloatField(write_only=True, required=False,
                                      help_text="Latitude ni kiriting (masalan: 39.654321)")
    longitude = serializers.FloatField(write_only=True, required=False,
                                       help_text="Longitude ni kiriting (masalan: 66.975432)")

    location = serializers.SerializerMethodField(read_only=True)


    images = TravelImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Travel
        fields = [ 'id',
            'title_uz', 'title_ru', 'title_en',
            'description_uz', 'description_ru', 'description_en',
            'address_uz', 'address_ru', 'address_en',
            'region',
            'latitude', 'longitude', 'location',
            'images', 'uploaded_images'
        ]
        extra_kwargs = {
            'region': {'help_text':"Region id ni kiriting"},
        }

    def get_location(self, obj) -> Dict[str, Optional[float]]:
        loc = obj.location or {}
        return {
            "latitude": loc.get("latitude", None),
            "longitude": loc.get("longitude", None)
        }


    def create(self, validated_data) -> Dict[str, Any]:
        uploaded_images = validated_data.pop('uploaded_images', [])
        latitude = validated_data.pop('latitude')
        longitude = validated_data.pop('longitude')


        validated_data['location'] = {
            "latitude": latitude,
            "longitude": longitude
        }

        travel = Travel.objects.create(**validated_data)

        for img in uploaded_images:
            TravelImage.objects.create(travel=travel, image=img)
        return travel


class TravelUpdateSerializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(
        queryset=Regions.objects.all(),
        required=False,
        allow_empty=True,
        help_text="Yangi Region id ni kiriting",
        default=""
    )

    title_uz = serializers.CharField(default="", help_text="Yangi Title uz ni kiriting")
    title_ru = serializers.CharField(default="", help_text="Yangi Title ru ni kiriting")
    title_en = serializers.CharField(default="", help_text="Yangi Title en ni kiriting")

    description_uz = serializers.CharField(default="", help_text="Yangi Description uz ni kiriting")
    description_ru = serializers.CharField(default="", help_text="Yangi Description ru ni kiriting")
    description_en = serializers.CharField(default="", help_text="Yangi Description en ni kiriting")

    address_uz = serializers.CharField(default="", help_text="Yangi Address uz ni kiriting")
    address_ru = serializers.CharField(default="", help_text="Yangi Adress ru ni kiriting")
    address_en = serializers.CharField(default="", help_text="Yangi Adress en ni kiriting")

    latitude = serializers.FloatField(write_only=True, required=False,
                                      help_text="Yangi Latitude ni kiriting (masalan: 39.654321)")
    longitude = serializers.FloatField(write_only=True, required=False,
                                       help_text="Yangi Longitude ni kiriting (masalan: 66.975432)")
    location = serializers.SerializerMethodField(read_only=True)

    images = TravelImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False, allow_empty=True, default=[]
    )

    class Meta:
        model = Travel
        fields = [
            'id',
            'title_uz', 'title_ru', 'title_en',
            'description_uz', 'description_ru', 'description_en',
            'address_uz', 'address_ru', 'address_en',
            'latitude', 'longitude',
            'location',
            'region',
            'images', 'uploaded_images',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_location(self, obj) -> Dict[str, Optional[float]]:
        loc = obj.location or {}
        return {
            "latitude": loc.get("latitude"),
            "longitude": loc.get("longitude")
        }


    def validate_region(self, value: Any) -> Regions:
        if not value:
            raise serializers.ValidationError("Region ID ni kiriting.")
        if not isinstance(value, Regions):
            raise serializers.ValidationError("Noto‘g‘ri Region ID.")
        return value


    def update(self, instance, validated_data) -> Dict[str, Any]:
        uploaded_images = validated_data.pop('uploaded_images', None)
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)

        location = instance.location or {}
        if latitude is not None:
            location['latitude'] = latitude
        if longitude is not None:
            location['longitude'] = longitude
        instance.location = location

        region = validated_data.pop('region', None)
        if region is not None:
            instance.region = region

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if uploaded_images is not None:
            instance.images.all().delete()
            for img in uploaded_images:
                TravelImage.objects.create(travel=instance, image=img)

        return instance

class TravelCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelComments
        fields = [
            'id', 'travel', 'comment', 'created_at',
        ]
        extra_kwargs = {
            'travel': {'help_text': "Travel id ni kiriting !"},
            'comment': {'help_text': "Comment ni kiriting !", 'default': ''},
        }
        read_only_fields = ['id', 'created_at']