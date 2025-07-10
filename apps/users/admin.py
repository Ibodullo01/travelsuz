from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ['id', 'username', 'email', 'phone_number', 'is_staff', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Qo‘shimcha ma’lumotlar', {'fields': ('phone_number', 'image')}),
    )
