from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class PlatformUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "username", "role", "is_staff", "is_active")
    ordering = ("email",)
    fieldsets = UserAdmin.fieldsets + (
        ("Profile", {"fields": ("phone", "avatar", "role")}),
    )
