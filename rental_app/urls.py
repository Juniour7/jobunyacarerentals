from django.urls import path
from . import views

urlpatterns = [
    path('user/register/', views.register_view, name='register'),
    path('user/login/', views.login_view, name='login'),
    path('user/logout/', views.logout_view, name='logout'),
    path('user/me/', views.me_view, name='me'),
    path('user/change_password/', views.change_password_view, name='change_password'),
    path('user/password-reset/', views.password_reset_request_view, name='password_reset'),
    path('user/passw0rd-reset-confirm/', views.password_reset_confirm_view, name='password_reset_confirm'),
]