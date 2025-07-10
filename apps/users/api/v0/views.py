from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView, ListAPIView, \
    get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated


from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import (
    RegisterSerializer, CustomTokenObtainPairSerializer,
    UserDetailSerializer, UserListSerializer, UserUpdateSerializer, LogoutSerializer
)

User = get_user_model()


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        tags=["Auth"],
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(description="Token + User Info", response=RegisterSerializer),
            400: OpenApiResponse(description="Validatsiya xatosi")
        },
        summary="Ro'yxatdan o'tish ",
        description="Ro‘yxatdan o‘tish va JWT token olish"
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
                    'image': user.image.url if user.image else None,
                    'phone_number': user.phone_number
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        tags=["Auth"],
        request=CustomTokenObtainPairSerializer,
        responses={200: OpenApiResponse(description="JWT tokenlar")},
        description="Login qilish va JWT token olish",
        summary="Tizimga Kirish"
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
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        tags=["Auth"],
        request=LogoutSerializer,
        responses={
            205: OpenApiResponse(description="Siz tizimdan chiqdingiz ✅"),
            400: OpenApiResponse(description="Yaroqsiz yoki muddati o‘tgan token")
        },
        summary="Tizimdan chiqish",
        description="Foydalanuvchini tizimdan chiqarish (Logout)"
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh']
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout bo‘ldi"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Yaroqsiz yoki muddati o‘tgan token"}, status=status.HTTP_400_BAD_REQUEST)



class DeleteUserView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'

    @extend_schema(
        tags=["Auth"],
        description="Admin tomonidan foydalanuvchini o‘chirish",
        summary="Foydalanuvchilarni o'chirish faqat Super admin o'chirishi mumkin",
        responses={
            204: OpenApiResponse(description="Foydalanuvchi o‘chirildi"),
            403: OpenApiResponse(description="O'zingizni o‘chira olmaysiz")
        }
    )
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            raise PermissionDenied("O'zingizni o‘chira olmaysiz.")
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @extend_schema(
        tags=["Auth"],
        description="Login bo‘lgan foydalanuvchining profilini olish",
        summary="Login bo'lgan foydalanuvchi uzining malumotlari",
        responses={200: UserDetailSerializer}
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)



class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]

    @extend_schema(
        tags=["Auth"],
        description="Register bo‘lgan foydalanuvchilar",
        summary="Register foydalanuvchilar ruyhati",
        responses={200: UserDetailSerializer}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)





class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        user = self.request.user
        if user.is_staff and 'pk' in self.kwargs:
            return get_object_or_404(User, pk=self.kwargs['pk'])
        return user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    @extend_schema(
        tags=["Auth"],
        summary="Foydalanuvchi ma'lumotlarini yangilash",
        description="Foydalanuvchi o'z ma'lumotlarini yoki admin boshqa foydalanuvchini yangilashi mumkin."
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        tags=["Auth"],
        summary="Foydalanuvchi ma'lumotlarini to'liq yangilash (PUT)",
        description="Foydalanuvchi o'z ma'lumotlarini to'liq almashtiradi."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
