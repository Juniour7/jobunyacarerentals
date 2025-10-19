from django.urls import path
from . import views

urlpatterns = [
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
]