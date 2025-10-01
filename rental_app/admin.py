from django.contrib import admin
from .models import UserProfile, Booking, Vehicle

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'license_number', 'roles', 'created_at']
    search_fields = ['full_name', 'creates_at', 'roles']


class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'vehicle', 'start_date', 'end_date', 'total_price', 'status', 'created_at']
    search_fields = ['user', 'vehicle', 'status', 'created_at']


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'car_type', 'seats', 'daily_rate', 'status', 'created_at']
    search_fields = ['name', 'model', 'car_type', 'created_at']


admin.site.register(UserProfile, UserAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Vehicle, VehicleAdmin)