from django.urls import path
from . import views

urlpatterns = [
    # =====================
    # 🚗 VEHICLE ENDPOINTS
    # =====================

    # Public (GET) and Admin (POST)
    path('vehicles/', views.VahicleListCreateView.as_view, name='vehicle-list-create'),

    # Public (GET) and Admin (PUT, DELETE)
    path('vehicles/<int:pk>/', views.vehicle_detail_view, name='vehicle-detail'),
]