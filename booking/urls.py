from django.urls import path
from . import views

urlpatterns = [
    # Customer endpoints
    path('bookings/', views.create_booking_view, name='booking-create'),   # POST - user creates booking
    path('my-bookings/', views.my_bookings, name='booking-my-list'),       # GET  - user views own bookings

    # Admin endpoints
    path('all-bookings/', views.all_booking_view, name='booking-all-list'),   # GET - admin: view all bookings
    path('bookings/<int:pk>/status/', views.update_booking_status_view, name='booking-status-update'),  # PUT - admin updates booking status


    # Location Endpoints
    path('locations/new/', views.location_create_view, name='location-create' ),
    path('locations/', views.location_list_view, name='location-list'),
    path('locations/<int:pk>/update/', views.update_location, name='location-update'),
    path('locations/<int:pk>/delete/', views.location_delete_view, name='location-delete'),

    # Damage Report Endpoints
    path('damage-reports/', views.DamageReportView.as_view(), name='damage-report-list-create'),
    path('admin/damage-reports/', views.AdminDamageReportView.as_view(), name='admin-damage-reports'),
    path('admin/damage-reports/<int:pk>/', views.AdminDamageReportDetailView.as_view, name='admin-damage-report-detail')
]