from email.policy import default

from django.contrib.admin.utils import help_text_for_field
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User=get_user_model()

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="Refresh token")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
        required=False,
        help_text='Parol kiriting. Katta, kichik harflar va belgilar, sonlardan qatnashgan bulsin',
        default=''
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password',
                  'first_name', 'last_name', 'image', 'phone_number')
        extra_kwargs = {
            'email': {
                'help_text': 'Email kiriting masalan: user@gmail.com',
                'default':''
            },
            'phone_number': {
                'required': False,
                'help_text': 'Telefon raqamingizni +998 bilan kiriting, masalan: +998941234567',
                'default':''
            },
            'username': {'help_text': 'username kiriting', 'default':''},
            'image': {'required': False, 'help_text': 'Rasm yuklang', },
            'first_name': {'help_text': 'Ismingizni kiriting', 'default':''},
            'last_name': {'help_text': 'Familiyangizni kiriting', 'default':''},

        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Bu username allaqachon ro‘yxatdan o‘tgan.")
        return value


    def create(self, validated_data):
        password = validated_data.pop('password')  # Default parol
        user = User(**validated_data)
        user.set_password(password)  # Hashlab saqlaydi
        user.save()
        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        data['message'] = "Tizimga muvaffaqiyatli kirdingiz"
        return data

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'image', 'phone_number']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'image']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'phone_number', 'image']
        extra_kwargs = {
            'email': {'help_text': 'Yangi email kiriting masalan: user@gmail.com', 'default': ''},
            'phone_number': {'required': False,
                             'help_text': 'Telefon raqamingizni +998 bilan kiriting, masalan: +998941234567',
                             'default': ''},
            'username': {'default': '', 'help_text': 'Yangi username kiriting'},
            'password': {'write_only': True, 'help_text': 'Yangi password kiriting', 'default': ''},
            'image': {'required': False, 'help_text': 'Yangi image kiriting', 'default': ''},
            'first_name': {'help_text': 'Yangi first name kiriting', 'default': ''},
            'last_name': {'help_text': 'Yangi last name kiriting', 'default': ''},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        if not user.is_staff:
            self.fields.pop('id')  # oddiy user uchun 'id'ni ko‘rsatmaymiz

    def validate_username(self, value):
        user = self.instance
        if not value:
            raise serializers.ValidationError("Username bo‘sh bo‘lmasligi kerak.")
        if User.objects.filter(username=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Bu username ro‘yxatdan o‘tgan. Boshqa username kiriting!")
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Parol bo‘sh bo‘lmasligi kerak.")
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

