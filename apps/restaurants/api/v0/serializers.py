from modeltranslation.utils import get_language
from rest_framework import serializers

from apps.restaurants.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    price_range = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'description', 'address', 'phone_number',
            'category', 'price_range', 'opening_time', 'closing_time',
            'image', 'location_url', 'tag', 'created_at', 'region'
        ]

    def get_language(self):
        return get_language() or 'uz'

    def get_name(self, obj):
        return getattr(obj, f'name_{self.get_language()}', obj.name)

    def get_description(self, obj):
        return getattr(obj, f'description_{self.get_language()}', obj.description)

    def get_address(self, obj):
        return getattr(obj, f'address_{self.get_language()}', obj.address)

    def get_category(self, obj):
        return getattr(obj, f'category_{self.get_language()}', obj.category)

    def get_price_range(self, obj):
        return getattr(obj, f'price_range_{self.get_language()}', obj.price_range)

    def get_tag(self, obj):
        return getattr(obj, f'tag_{self.get_language()}', obj.tag)

    def get_region(self, obj):
        return getattr(obj.region, f'name_{self.get_language()}', obj.region.name)

class RestaurantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name_uz', 'name_ru', 'name_en',
            'description_uz', 'description_ru', 'description_en',
            'address_uz', 'address_ru', 'address_en',  # 3 tilli address
            'phone_number', 'price_range_uz', 'price_range_ru', 'price_range_en',
            'category_uz', 'category_ru', 'category_en',
            'image', 'location_url', 'tag_uz', 'tag_ru', 'tag_en', 'created_at', 'region'
        ]

class RestaurantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name_uz', 'name_ru', 'name_en',
            'description_uz', 'description_ru', 'description_en',
            'address_uz', 'address_ru', 'address_en',  # 3 tilli address
            'phone_number',  'price_range_uz', 'price_range_ru', 'price_range_en',
            'category_uz', 'category_ru', 'category_en',
            'image', 'location_url', 'tag_uz', 'tag_ru', 'tag_en', 'created_at', 'region'
        ]

    # def update(self, instance, validated_data):
    #     instance = Restaurant.objects.get(pk=instance.id)
    #     request_id = validated_data.get('id', None)
    #
    #     if request_id != instance.id:
    #         raise serializers.ValidationError("ID mos kelmadi. Yangilashga ruxsat yo‘q.")
    #
    #     return super().update(instance, validated_data)



