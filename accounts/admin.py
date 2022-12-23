from pyexpat import model
from django.utils.translation import gettext_lazy as _

from django.contrib import admin
from accounts.models import User, AccessToken, Contact
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class AccessTokenAdmin(admin.TabularInline):
    """create tabular access raws"""
    model = AccessToken
    list_display = ['idencode', 'key', 'active']


class UserAdminNew(UserAdmin):
    """Override user admin view"""
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("extra"), {"fields": ("profile_pic",)}),
    )
    inlines = [AccessTokenAdmin]


admin.site.register(User, UserAdminNew)
admin.site.register(Contact)
