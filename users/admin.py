from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import StoreUser


@admin.register(StoreUser)
class UsersAdmin(UserAdmin):
    """Админка пользователя."""
