from django.urls import path
from . import views

urlpatterns = [

    # ===========================
    # AUTHENTICATION ENDPOINTS
    # ===========================
    # Public access (AllowAny)
    path('user/register/', views.register_view, name='user-register'),  # POST - register new user

    # New Endpoints
    path('user/verify-email/', views.verify_email, name='verify-email'),
    path('user/resend-verification/', views.resend_verification_email_view, name='resend-verification'),

    path('user/login/', views.login_view, name='user-login'),          # POST - login
    path('user/password-reset/', views.password_reset_request_view, name='password-reset-request'),  # POST
    path('user/password-reset-confirm/', views.password_reset_confirm_view, name='password-reset-confirm'),  # POST

    # Authenticated users only
    path('user/logout/', views.logout_view, name='user-logout'),       # POST - logout
    path('user/me/', views.me_view, name='user-profile'),              # GET - current user info
    path('user/change-password/', views.change_password_view, name='user-change-password'),  # POST

    # Admin-only user management
    path('user/customer-list/', views.customer_list, name='user-list'),  # GET - admin: list all user
]
