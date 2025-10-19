from django.urls import path
from . import views

urlpatterns = [
    # Customer endpoints
    path('bookings/', views.create_booking_view, name='booking-create'),   # POST - user creates booking
    path('my-bookings/', views.my_bookings, name='booking-my-list'),       # GET  - user views own bookings

    # Admin endpoints
    path('all-bookings/', views.all_booking_view, name='booking-all-list'),   # GET - admin: view all bookings
    path('bookings/<int:pk>/status/', views.update_booking_status_view, name='booking-status-update'),  # PUT - admin updates booking status
]