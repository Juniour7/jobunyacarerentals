from django.urls import path
from . import views

urlpatterns = [

    # ===========================
    # AUTHENTICATION ENDPOINTS
    # ===========================
    # Public access (AllowAny)
    path('user/register/', views.register_view, name='user-register'),  # POST - register new user
    path('user/login/', views.login_view, name='user-login'),          # POST - login
    path('user/password-reset/', views.password_reset_request_view, name='password-reset-request'),  # POST
    path('user/password-reset-confirm/', views.password_reset_confirm_view, name='password-reset-confirm'),  # POST

    # Authenticated users only
    path('user/logout/', views.logout_view, name='user-logout'),       # POST - logout
    path('user/me/', views.me_view, name='user-profile'),              # GET - current user info
    path('user/change-password/', views.change_password_view, name='user-change-password'),  # POST

    # Admin-only user management
    path('user/customer-list/', views.customer_list, name='user-list'),  # GET - admin: list all users


    # =====================
    # 🚗 VEHICLE ENDPOINTS
    # =====================

    # Public (GET) and Admin (POST)
    path('vehicles/', views.vehicle_list_create_view, name='vehicle-list-create'),
    #   GET  - list all vehicles (public)
    #   POST - add a new vehicle (admin only)

    # Public (GET) and Admin (PUT, DELETE)
    path('vehicles/<int:pk>/', views.vehicle_detail_view, name='vehicle-detail'),
    #   GET    - retrieve a single vehicle (public)
    #   PUT    - update a vehicle (admin only)
    #   DELETE - delete a vehicle (admin only)


    # =====================
    # 📘 BOOKING ENDPOINTS
    # =====================

    # Customer endpoints
    path('bookings/', views.create_booking_view, name='booking-create'),   # POST - user creates booking
    path('my-bookings/', views.my_bookings, name='booking-my-list'),       # GET  - user views own bookings

    # Admin endpoints
    path('all-bookings/', views.all_booking_view, name='booking-all-list'),   # GET - admin: view all bookings
    path('bookings/<int:pk>/status/', views.update_booking_status_view, name='booking-status-update'),  # PUT - admin updates booking status
]
