from rest_framework import serializers
from .models import Vehicle


# Serializers for vehicle model
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'id',
            'name',
            'model',
            'car_type',
            'description',
            'seats',
            'transmission',
            'fuel_type',
            'daily_rate',
            'status',
            'features',
            'image',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']