from django.contrib import admin
from .models import Vehicle, VehicleImage

# Register your models here.
class VehicleImageInline(admin.TabularInline):
    """Allows adding multiple VehicleImage objects directly in the Vehicle form."""
    model = VehicleImage
    extra = 1  # how many empty forms to show
    fields = ('image', 'uploaded_at')
    readonly_fields = ('uploaded_at',)

class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'car_type', 'seats', 'daily_rate', 'status', 'created_at']
    search_fields = ['name', 'model', 'car_type', 'created_at']
    inlines = [VehicleImageInline]


@admin.register(VehicleImage)
class VehicleImageAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'image', 'uploaded_at']
    search_fields = ['vehicle__name']