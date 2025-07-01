from tokenize import TokenError

from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import DestroyAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.schemas import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg import openapi
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()



class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
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
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# LOGIN

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed:
            return Response({'error': 'Login yoki parol noto‘g‘ri'},
                            status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)



class DeleteUserView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]  # faqat admin o‘chira oladi
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"message": "Foydalanuvchi o‘chirildi"},
                        status=status.HTTP_204_NO_CONTENT)

# LOGOUT
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    @swagger_auto_schema(
        operation_description="Foydalanuvchini tizimdan chiqarish (logout)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Refresh tokenni kiriting"
                )
            }
        ),
        responses={
            205: openapi.Response( description="Siz tizimdan chiqdingiz ✅"),

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