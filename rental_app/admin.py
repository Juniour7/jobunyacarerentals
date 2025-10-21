from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile, Admin


@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):
    model = UserProfile
    list_display = ('email', 'full_name', 'roles', 'is_staff', 'is_superuser', 'created_at')
    list_filter = ('roles', 'is_staff', 'is_superuser', 'created_at')
    ordering = ('-created_at',)
    search_fields = ('email', 'full_name', 'license_number')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'phone_number', 'license_number')}),
        (_('Permissions'), {'fields': ('roles', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone_number', 'license_number', 'password1', 'password2', 'roles', 'is_staff', 'is_superuser'),
        }),
    )

    # Use email for login
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # Hide username field
        for name, opts in fieldsets:
            if 'username' in opts.get('fields', ()):
                opts['fields'] = tuple(f for f in opts['fields'] if f != 'username')
        return fieldsets


@admin.register(Admin)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')