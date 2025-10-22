from rest_framework import serializers

from .models import Vehicle, VehicleImage


# Serializers for vehicle model
class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ['id', 'image', 'uploaded_at']



class VehicleSerializer(serializers.ModelSerializer):
    images = VehicleImageSerializer(many=True, read_only=True)

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
            'images',
            'min_days',
            'engine',
            'engine_torque',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']