from django.urls import path
from . import views

urlpatterns = [
    path('user/register/', views.register_view, name='register')
]