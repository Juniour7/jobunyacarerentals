from django.urls import path
from . import views

urlpatterns = [
    # User login endpoints
    path('user/register/', views.register_view, name='register'),
    path('user/login/', views.login_view, name='login'),
    path('user/logout/', views.logout_view, name='logout'),
    path('user/me/', views.me_view, name='me'),
    path('user/change_password/', views.change_password_view, name='change_password'),
    path('user/password-reset/', views.password_reset_request_view, name='password_reset'),
    path('user/passw0rd-reset-confirm/', views.password_reset_confirm_view, name='password_reset_confirm'),

    # Vehicle Endpoints
    path('vehicle/', views.vehicle_list_create_view, name='vehicle-list'),
    path('vehicle/<int:pk>/', views.vehicle_detail_view, name='vehicle-detail'),

    # Booking endpoint
    path('bookings/', views.create_booking_view, name='booking-create'),
    path('my-bookings/', views.my_bookings, name='my-booking'),
    path('all-bookings/', views.all_booking_view, name='all-booking'),
    path('bookings/<int:pk>/status/', views.update_booking_status_view, name='update-booking-status')
]