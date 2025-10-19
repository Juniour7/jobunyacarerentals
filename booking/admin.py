from django.contrib import admin
from .models import Booking

# Register your models here.
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'vehicle', 'start_date', 'end_date', 'total_price', 'status', 'created_at']
    search_fields = ['user', 'vehicle', 'status', 'created_at']

admin.site.register(Booking, BookingAdmin)