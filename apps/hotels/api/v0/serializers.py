from rest_framework import serializers
from apps.hotels.models import Regions, Hotel

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regions
        fields = ['id', 'name']

    def get_lang(self):
        request = self.context.get('request')
        if request:
            return request.query_params.get('lang','uz')
        return 'uz'

    def get_name(self, obj):
        lang = self.get_lang()
        return getattr(obj, f'name_{lang}', obj.name_uz)


class RegionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regions
        fields = ['id', 'name_uz', 'name_ru', 'name_en']

class HotelSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = [
            'id',
            'title',
            'description',
            'address',
            'phone_number',
            'phone_number_2',
            'price',
            'image',
            'location_url',
            'tag',
            'created_at',
            'region'
        ]

    def get_lang(self):
        request = self.context.get('request')
        if request:
            return request.query_params.get('lang', 'uz')  # Default: uz
        return 'uz'

    def get_title(self, obj):
        lang = self.get_lang()
        return getattr(obj, f'title_{lang}', obj.title_uz)

    def get_description(self, obj):
        lang = self.get_lang()
        return getattr(obj, f'description_{lang}', obj.description_uz)

    def get_address(self, obj):
        lang = self.get_lang()
        return getattr(obj, f'address_{lang}', obj.address_uz)

    def get_tag(self, obj):
        lang = self.get_lang()
        return getattr(obj, f'tag_{lang}', obj.tag_uz)

    def get_region(self, obj):
        lang = self.get_lang()
        region = obj.region
        return {
            "id": region.id,
            "name": getattr(region, f"name_{lang}", region.name)
        }


class HotelCreateSerializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(
        queryset=Regions.objects.all(),
        help_text="Regionni tanlang"
    )
    image = serializers.ImageField()
    class Meta:
        model = Hotel
        fields = [
            'title_uz', 'title_ru', 'title_en',
            'description_uz', 'description_ru', 'description_en',
            'address_uz', 'address_ru', 'address_en',  # 3 tilli address
            'phone_number', 'phone_number_2', 'price',
            'image', 'location_url', 'region', 'tag_uz', 'tag_ru', 'tag_en'
        ]


class HotelUpdateSerializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(
        queryset=Regions.objects.all(),
        required=False
    )
    image = serializers.ImageField(required=False)
    class Meta:
        model = Hotel
        fields = [
            'id',
            'title_uz', 'title_ru', 'title_en',
            'description_uz', 'description_ru', 'description_en',
            'address_uz', 'address_ru', 'address_en',  # 3 tilli address
            'phone_number', 'phone_number_2', 'price',
            'image', 'location_url', 'region', 'tag_uz', 'tag_ru', 'tag_en'
        ]
