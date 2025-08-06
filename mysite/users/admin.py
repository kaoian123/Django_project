"""users app 的後台管理設定。"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    """自定義用戶管理界面。"""
    list_display = (
        "email",
        "username",
        "is_staff",
        "is_active",
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2"),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["email"].required = True
        return form


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
