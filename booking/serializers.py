from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Booking, DamageReport
from vehicles.models import Vehicle

from rental_app.serializers import UserSerializer
from vehicles.serializers import VehicleSerializer

UserProfile = get_user_model()


# Serializer for the booking model
class BookingSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)
    vehicle_name = serializers.CharField(source='vehicle.name', read_only=True)
    vehicle_image = serializers.ImageField(source='vehicle.image', read_only=True)
    daily_rate = serializers.DecimalField(source='vehicle.daily_rate', read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Booking
        fields = [
            'id',
            'user',
            'pickup_location',
            'dropoff_location'
            'user_info',
            'vehicle',
            'vehicle_name',
            'vehicle_image',
            'start_date',
            'end_date',
            'total_price',
            'status',
            'daily_rate',
            'created_at'
        ]    
        read_only_fields = ['id', 'user', 'pickup_location', 'dropoff_location', 'user_info', 'status', 'vehicle_name', 'vehicle_image', 'daily_rate', 'created_at', 'total_price'] # fields we wouldnt wish the user to edit

    def create(self, validated_data):
        # Aurtomatically calculate total price
        # Total price = vehicle.dailyrate * number of days  
        request = self.context.get('request')
        user = request.user if request else None

        vehicle = validated_data['vehicle']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        min_days = vehicle.min_days

        # validation, end_date must not be before start_date
        if end_date < start_date:
            raise serializers.ValidationError("End date cannot be before start date")
        
        # Calculate number of days
        number_of_days = (end_date - start_date).days + 1

        if number_of_days < min_days:
            raise serializers.ValidationError(f"Number of days cant be less than {min_days} period")

        # compute total price
        total_price = vehicle.daily_rate * number_of_days

        #create the booking
        booking = Booking.objects.create(
            user=user,
            vehicle=vehicle,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            status='pending'
        )
        return booking 


class DamageReportSerializer(serializers.ModelSerializer):
    booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.none())
    booking_details = BookingSerializer(source='booking', read_only=True)
    user_details = UserSerializer(source='booking.user', read_only=True)
    vehicle_details = serializers.SerializerMethodField()

    class Meta:
        model = DamageReport
        fields = ['id', 'booking', 'booking_details', 'user_details', 'vehicle_details', 'description', 'status', 'created_at']
        read_only_fields = ['id', 'created_at', 'booking_details', 'user_details', 'vehicle_details']

    def get_vehicle_details(self, obj):
        if not obj.booking or not obj.booking.vehicle:
            return None
        vehicle = obj.booking.vehicle
        return {
            "id": vehicle.id,
            "name": vehicle.name,
            "image": vehicle.image.url if vehicle.image else None,
            "daily_rate": str(vehicle.daily_rate),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            if getattr(request.user, 'roles', None) == 'admin':
                self.fields['booking'].queryset = Booking.objects.all()
            else:
                self.fields['booking'].queryset = Booking.objects.filter(user=request.user)
            if getattr(request.user, 'roles', None) != 'admin':
                self.fields['status'].read_only = True
        else:
            self.fields['booking'].queryset = Booking.objects.none()

    def validate_booking(self, booking):
        if hasattr(booking, 'damagereport'):
            raise serializers.ValidationError("A damage report already exists for this booking.")
        return booking

