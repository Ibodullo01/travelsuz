from django.urls import path
from .views import (RegisterView, LoginView, LogoutView, DeleteUserView,
                    UserDetailView, UserListView, UserUpdateAPIView)


app_name = 'users_api'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),
    path('user/me/', UserDetailView.as_view(), name='user_detail'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('user_update/', UserUpdateAPIView.as_view(), name='update_user'),
]

