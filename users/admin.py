from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        # 　個人情報欄にdescriptionを追加
        (_('Personal info'), {'fields': ('email', 'description', 'icon', 'follow', 'follower', 'register_tag')}),

        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),

        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),

    )


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
