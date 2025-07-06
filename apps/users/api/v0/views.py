from tokenize import TokenError
from rest_framework.exceptions import PermissionDenied
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.auth import get_user_model
from .serializers import (RegisterSerializer, CustomTokenObtainPairSerializer,
                          UserDetailSerializer)


User = get_user_model()


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        tags=["Auth"],
        request_body=RegisterSerializer,
        responses={201: openapi.Response('Token + User Info', RegisterSerializer)},
        operation_description="Ro‘yxatdan o‘tish va JWT token olish"
    )
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'image': user.image.url,
                    'phone_number': user.phone_number
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        tags=["Auth"],
        operation_description="Login qilish va JWT token olish",
        request_body=CustomTokenObtainPairSerializer,
        responses={200: openapi.Response("JWT tokenlar")}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed:
            return Response({'error': 'Login yoki parol noto‘g‘ri'},
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=["Auth"],
        operation_description="Foydalanuvchini tizimdan chiqarish (Logout)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Refresh token"
                )
            }
        ),
        responses={
            205: openapi.Response(description="Siz tizimdan chiqdingiz ✅"),
            400: openapi.Response(description="Yaroqsiz yoki muddati o‘tgan token")
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout bo‘ldi"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Yaroqsiz yoki muddati o‘tgan token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'

    @swagger_auto_schema(
        tags=["Auth"],
        operation_description="Admin tomonidan foydalanuvchini o‘chirish",
        responses={204: openapi.Response(description="Foydalanuvchi o‘chirildi")}
    )
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            raise PermissionDenied("O'zingizni o'chira olmaysiz.")
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]


    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        tags=["Auth"],
        operation_description="Login bo‘lgan foydalanuvchining profilini olish"
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)