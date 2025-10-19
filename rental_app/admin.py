from django.contrib import admin
from .models import UserProfile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'license_number', 'roles', 'created_at']
    search_fields = ['full_name', 'creates_at', 'roles']



admin.site.register(UserProfile, UserAdmin)