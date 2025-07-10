from curses.ascii import isdigit
from decimal import Decimal, InvalidOperation
from typing import Dict, Optional, Any, List

from drf_spectacular.utils import extend_schema_field
from modeltranslation.utils import get_language
from rest_framework import serializers
from apps.hotels.models import Regions, Hotel, HotelImage, HotelComment
from apps.travels.models import TravelImage


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regions
        fields = ['id', 'name_uz', 'name_ru', 'name_en']
        extra_kwargs = {
            'name_uz': {'help_text': 'Name uz ni kiriting', 'default':''},
            'name_ru': {'help_text': 'Name ru ni kiriting', 'default':''},
            'name_en': {'help_text': 'Name en ni kiriting', 'default':''}

        }

    def get_lang(self) -> str:
        request = self.context.get('request')
        if request:
            return request.query_params.get('lang','uz')
        return 'uz'

    def get_name(self, obj) -> str:
        lang = self.get_lang()
        return getattr(obj, f'name_{lang}', obj.name_uz)


class RegionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regions
        fields = ['id', 'name_uz', 'name_ru', 'name_en']
        extra_kwargs = {
            'name_uz': {'help_text': 'Name uz ni kiriting', 'default':''},
            'name_ru': {'help_text': 'Name ru ni kiriting', 'default':''},
            'name_en': {'help_text': 'Name en ni kiriting', 'default':''}

        }


class HotelSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = [
            'id',
            'title',
            'description',
            'address',
            'phone_number',
            'price',
            'images',
            'location',
            'created_at',
            'region',
            'views'
        ]

    def get_lang(self) -> str:
        request = self.context.get('request')
        if request:
            return request.query_params.get('lang', 'uz')  # Default: uz
        return 'uz'

    def get_title(self, obj) -> str:
        lang = self.get_lang()
        return getattr(obj, f'title_{lang}', obj.title_uz)

    def get_description(self, obj) -> str:
        lang = self.get_lang()
        return getattr(obj, f'description_{lang}', obj.description_uz)

    def get_address(self, obj) -> str:
        lang = self.get_lang()
        return getattr(obj, f'address_{lang}', obj.address_uz)



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

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelImage
        fields = ['id', 'image']


class HotelCreateSerializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(
        queryset=Regions.objects.all(),
        help_text="Regionni id kiriting",
        default=""
    )

    title_uz = serializers.CharField(default="", help_text="Title uz ni kiriting")
    title_ru = serializers.CharField(default="", help_text="Title ru ni kiriting")
    title_en = serializers.CharField(default="", help_text="Title en ni kiriting")

    description_uz = serializers.CharField(default="", help_text="Description uz ni kiriting")
    description_ru = serializers.CharField(default="", help_text="Description ru ni kiriting")
    description_en = serializers.CharField(default="", help_text="Description en ni kiriting")

    address_uz = serializers.CharField(default="", help_text="Address uz ni kiriting")
    address_ru = serializers.CharField(default="", help_text="Adress ru ni kiriting")
    address_en = serializers.CharField(default="", help_text="Adress en ni kiriting")
    phone_number = serializers.CharField(default="", help_text="Phone number ni kiriting -> : +998XX1234567")
    price = serializers.CharField(default="", help_text="Price ni kiriting (masalan: 156451)")

    latitude = serializers.FloatField(write_only=True, help_text="Latitude ni kiriting (masalan: 39.654321)")
    longitude = serializers.FloatField(write_only=True, help_text="Longitude ni kiriting (masalan: 66.975432)")

    location = serializers.SerializerMethodField(read_only=True)

    images = HotelImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )


    class Meta:
        model = Hotel
        fields = [
            'title_uz', 'title_ru', 'title_en',
            'description_uz', 'description_ru', 'description_en',
            'address_uz', 'address_ru', 'address_en',  # 3 tilli address
            'phone_number', 'price', 'region',
            'location', 'latitude', 'longitude', 'images', 'uploaded_images',

        ]
        read_only_fields = ['id', 'created_at']



    def get_location(self, obj) -> Dict[str, Optional[float]]:
        loc = obj.location or {}
        return {
            "latitude": loc.get("latitude", None),
            "longitude": loc.get("longitude", None)
        }

    def validate_price(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError("Narxni kiriting.")

        try:
            price = Decimal(value)
        except (InvalidOperation, TypeError):
            raise serializers.ValidationError("Narx raqam formatida bo‘lishi kerak. Masalan: 150000")

        if price <= 0:
            raise serializers.ValidationError("Narx 0 dan katta bo‘lishi kerak.")

        return value


    def create(self, validated_data) -> Dict[str, Any]:
        uploaded_images = validated_data.pop('uploaded_images', [])
        latitude = validated_data.pop('latitude')
        longitude = validated_data.pop('longitude')


        validated_data['location'] = {
            "latitude": latitude,
            "longitude": longitude
        }

        hotel = Hotel.objects.create(**validated_data)

        for img in uploaded_images:
            HotelImage.objects.create(hotel=hotel, image=img)
        return hotel



class HotelUpdateSerializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(
        queryset=Regions.objects.all(),
        required=False,
        allow_empty=True,
        help_text="Region id ni kiriting",
        default=""
    )

    latitude = serializers.FloatField(write_only=True, required=False,
                                      help_text="Yangi Latitude ni kiriting (masalan: 39.654321)")
    longitude = serializers.FloatField(write_only=True, required=False,
                                       help_text="Yangi Longitude ni kiriting (masalan: 66.975432)")
    location = serializers.SerializerMethodField(read_only=True)

    images = HotelImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False, allow_empty=True, default=[]
    )

    class Meta:
        model = Hotel
        fields = [
            'id',
            'title_uz', 'title_ru', 'title_en',
            'description_uz', 'description_ru', 'description_en',
            'address_uz', 'address_ru', 'address_en',  # 3 tilli address
            'phone_number', 'price', 'region',
            'location', 'latitude', 'longitude', 'images', 'uploaded_images',
        ]
        read_only_fields = ['id', 'created_at']

        extra_kwargs = {
            'title_uz': {'help_text': "Yangi title uz ni kiriting !", 'default': ''},
            'title_ru': {'help_text': "Yangi title ru ni kiriting !", 'default': ''},
            'title_en': {'help_text': "Yangi title ni kiriting !", 'default': ''},
            'description_uz': {'help_text': "Yangi Description uz ni kiriting !", 'default': ''},
            'description_ru': {'help_text': "Yangi Description ru ni kiriting !", 'default': ''},
            'description_en': {'help_text': "Yangi Description ni kiriting !", 'default': ''},
            'address_uz': {'help_text': "Yangi Address uz ni kiriting !", 'default': ''},
            'address_ru': {'help_text': "Yangi Address ru ni kiriting !", 'default': ''},
            'address_en': {'help_text': "Yangi Address en ni kiriting !", 'default': ''},
            'phone_number': {'help_text': "Yangi Phone number ni kiriting !", 'default': ''},
            'price': {'help_text': "Yangi Price ni kiriting (masalan : 1321212)!",'default': ''},
            'image': {'help_text': "Yangi Image ni kiriting !", 'default': ''},
            'region': {'help_text': "Yangi Region id ni kiriting !", 'default': ''},

        }

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

    def validate_price(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError("Narxni kiriting.")

        try:
            price = Decimal(value)
        except (InvalidOperation, TypeError):
            raise serializers.ValidationError("Narx raqam formatida bo‘lishi kerak. Masalan: 150000")

        if price <= 0:
            raise serializers.ValidationError("Narx 0 dan katta bo‘lishi kerak.")

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


        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if uploaded_images is not None:
            instance.images.all().delete()
            for img in uploaded_images:
                HotelImage.objects.create(hotel=instance, image=img)

        return instance


class HotelCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelComment
        fields = ['id', 'hotel', 'text', 'created_at']
        extra_kwargs = {
            'hotel': {'help_text': "hotel id ni kiriting !"},
            'text': {'help_text': "Comment text ni kiriting !", 'default':''},
        }
        read_only_fields = ['id', 'created_at']