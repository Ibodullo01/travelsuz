from typing import List, Dict, Optional, Any

from drf_spectacular.utils import extend_schema_field
from modeltranslation.utils import get_language
from rest_framework import serializers

from apps.hotels.models import Regions
from apps.restaurants.models import Restaurant, RestaurantImage, RestaurantComments


class RestaurantSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    price_range = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'description', 'address', 'phone_number',
            'category', 'price_range', 'opening_time', 'closing_time',
            'images', 'location',  'region', 'created_at','views'
        ]

    def get_language(self) -> str:
        return get_language() or 'uz'

    def get_name(self, obj) -> str:
        return getattr(obj, f'name_{self.get_language()}', obj.name)

    def get_description(self, obj) -> str:
        return getattr(obj, f'description_{self.get_language()}', obj.description)

    def get_address(self, obj) -> str:
        return getattr(obj, f'address_{self.get_language()}', obj.address)

    def get_category(self, obj) -> str:
        return getattr(obj, f'category_{self.get_language()}', obj.category)

    def get_price_range(self, obj) -> str:
        return getattr(obj, f'price_range_{self.get_language()}', obj.price_range)

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


class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImage
        fields = ['id', 'image']


class RestaurantCreateSerializer(serializers.ModelSerializer):

    latitude = serializers.FloatField(write_only=True, required=False,
                                      help_text="Latitude ni kiriting (masalan: 39.654321)")
    longitude = serializers.FloatField(write_only=True, required=False,
                                       help_text="Longitude ni kiriting (masalan: 66.975432)")

    location = serializers.SerializerMethodField(read_only=True)

    images = RestaurantImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name_uz', 'name_ru', 'name_en',
            'description_uz', 'description_ru', 'description_en',
            'address_uz', 'address_ru', 'address_en',  # 3 tilli address
            'phone_number', 'price_range_uz', 'price_range_ru', 'price_range_en',
            'category_uz', 'category_ru', 'category_en',
            'images', 'location', 'created_at', 'region', 'opening_time', 'closing_time',
            'latitude', 'longitude','uploaded_images'
        ]
        extra_kwargs = {
            'name_uz': {'help_text':"Name uz ni kiriting !", 'default':'' },
            'name_ru': {'help_text':"Name ru ni kiriting !", 'default':'' },
            'name_en': {'help_text':"Name ni kiriting !", 'default':'' },
            'description_uz': {'help_text':"Description uz ni kiriting !", 'default':'' },
            'description_ru': {'help_text':"Description ru ni kiriting !", 'default':'' },
            'description_en': {'help_text':"Description ni kiriting !", 'default':'' },
            'address_uz': {'help_text':"Address uz ni kiriting !", 'default':'' },
            'address_ru': {'help_text':"Address ru ni kiriting !", 'default':'' },
            'address_en': {'help_text':"Address en ni kiriting !", 'default':'' },
            'phone_number': {'help_text':"Phone number ni kiriting !", 'default':'' },
            'price_range_uz': {'help_text':"Price range uz ni kiriting (Arzon, O'rta, Qimmat)!", 'default':'' },
            'price_range_ru': {'help_text':"Price range ru ni kiriting (Arzon, O'rta, Qimmat)!", 'default':'' },
            'price_range_en': {'help_text':"Price range en ni kiriting (Arzon, O'rta, Qimmat)!", 'default':'' },
            'category_uz': {'help_text':"Category uz kiriting !", 'default':'' },
            'category_ru': {'help_text':"Category ru kiriting !", 'default':'' },
            'category_en': {'help_text':"Category en kiriting !", 'default':'' },
            'images': {'help_text':"Image ni kiriting !", 'default':'' },
            'region': {'help_text':"Region id ni kiriting !", 'default':'' },
            'opening_time': {'help_text':"Opening timeni 08:00 shu tarzda kiriting !"},
            'closing_time': {'help_text':"Closing timeni 22:10 shu tarzda kiriting !"},

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

        restaurant = Restaurant.objects.create(**validated_data)

        for img in uploaded_images:
            RestaurantImage.objects.create(restaurant=restaurant, image=img)
        return restaurant





class RestaurantUpdateSerializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(
        queryset=Regions.objects.all(),
        required=False,
        allow_empty=True,
        help_text="Yangi region id ni kiriting",
        default=""
    )

    latitude = serializers.FloatField(write_only=True, required=False,
                                      help_text="Yangi Latitude ni kiriting (masalan: 39.654321)")
    longitude = serializers.FloatField(write_only=True, required=False,
                                       help_text="Yangi Longitude ni kiriting (masalan: 66.975432)")
    location = serializers.SerializerMethodField(read_only=True)

    images = RestaurantImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False, allow_empty=True, default=[]
    )

    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name_uz', 'name_ru', 'name_en',
            'description_uz', 'description_ru', 'description_en',
            'address_uz', 'address_ru', 'address_en',  # 3 tilli address
            'phone_number', 'price_range_uz', 'price_range_ru', 'price_range_en',
            'category_uz', 'category_ru', 'category_en',
            'images', 'location', 'created_at', 'region', 'opening_time', 'closing_time',
            'latitude', 'longitude','uploaded_images'
        ]
        read_only_fields = ['id', 'created_at']

        extra_kwargs = {
            'name_uz': {'help_text': "Yangi Name uz ni kiriting !", 'default': ''},
            'name_ru': {'help_text': "Yangi Name ru ni kiriting !", 'default': ''},
            'name_en': {'help_text': "Yangi Name ni kiriting !", 'default': ''},
            'description_uz': {'help_text': "Yangi Description uz ni kiriting !", 'default': ''},
            'description_ru': {'help_text': "Yangi Description ru ni kiriting !", 'default': ''},
            'description_en': {'help_text': "Yangi Description ni kiriting !", 'default': ''},
            'address_uz': {'help_text': "Yangi Address uz ni kiriting !", 'default': ''},
            'address_ru': {'help_text': "Yangi Address ru ni kiriting !", 'default': ''},
            'address_en': {'help_text': "Yangi Address en ni kiriting !", 'default': ''},
            'phone_number': {'help_text': "Yangi Phone number ni kiriting !", 'default': ''},
            'price_range_uz': {'help_text': "Yangi Price range uz ni kiriting (Arzon, O'rta, Qimmat)!", 'default': ''},
            'price_range_ru': {'help_text': "Yangi Price range ru ni kiriting (Arzon, O'rta, Qimmat)!", 'default': ''},
            'price_range_en': {'help_text': "Yangi Price range en ni kiriting (Arzon, O'rta, Qimmat)!", 'default': ''},
            'category_uz': {'help_text': "Yangi Category uz kiriting !", 'default': ''},
            'category_ru': {'help_text': "Yangi Category ru kiriting !", 'default': ''},
            'category_en': {'help_text': "Yangi Category en kiriting !", 'default': ''},
            'image': {'help_text': "Yangi Image ni kiriting !", 'default': ''},
            'opening_time': {'help_text': "Yangi Opening timeni 08:00 shu tarzda kiriting !"},
            'closing_time': {'help_text': "Yangi Closing timeni 22:10 shu tarzda kiriting !"},

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
                RestaurantImage.objects.create(restaurant=instance, image=img)

        return instance



class RestaurantCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantComments
        fields = [
            'id', 'restaurant', 'comment','created_at'
        ]
        extra_kwargs = {
            'restaurant': {'help_text': "Restaurant id ni kiriting !"},
            'comment': {'help_text': "Comment ni kiriting !", 'default': ''},
        }