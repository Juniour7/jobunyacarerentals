from django.contrib import admin
from .models import Vehicle, VehicleImage

class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 1
    fields = ('image', 'uploaded_at')
    readonly_fields = ('uploaded_at',)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'car_type', 'seats', 'daily_rate', 'status', 'created_at']
    search_fields = ['name', 'model', 'car_type', 'created_at']
    inlines = [VehicleImageInline]


@admin.register(VehicleImage)
class VehicleImageAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'image', 'uploaded_at']
    search_fields = ['vehicle__name']
