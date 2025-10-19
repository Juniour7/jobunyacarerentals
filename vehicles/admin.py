from django.contrib import admin
from .models import Vehicle

# Register your models here.
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'car_type', 'seats', 'daily_rate', 'status', 'created_at']
    search_fields = ['name', 'model', 'car_type', 'created_at']

admin.site.register(Vehicle, VehicleAdmin)