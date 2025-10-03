from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password # for password validations
from datetime import timedelta

# Models
from .models import Booking, Vehicle, Admin, UserProfile

user = get_user_model()

# Serializers for User profile models
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        # fields to expose
        fields = ['id', 'email', 'full_name', 'phone_number', 'license_number', 'roles', 'agree_terms', 'created_at' ]
        read_only_fields = ['id', 'created_at']
    


class RegisterSerializer(serializers.ModelSerializer):
    """
    To handle regitration of new customers
    """
    password = serializers.CharField(write_only = True, required = True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True, required = True, help_text='Repeat Password')

    class Meta:
        model = user
        fields = [
            'full_name',
            'email',
            'phone_number',
            'license_number',
            'roles',
            'agree_terms',
            'password',
            'password2',
        ]
    
    def validate(self,attrs):
        # password match check
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        
        # must accept terms
        if not attrs.get('agree_terms'):
            raise serializers.ValidationError({"agree_terms": "You must agree to terms"})
        
        return attrs
    
    def validate_email(self, value):
        """
        Check of email is already in use before saving
        """
        if UserProfile.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists")
        return value
    
    def create(self, validated_data):
        # Remove the second password and set the password correctly
        validated_data.pop('password2', None)
        raw_password = validated_data.pop('password')
        user = UserProfile(**validated_data)
        user.set_password(raw_password)
        user.save()

        # when user is registered as admin
        if user.roles == 'admin':
            Admin.objects.create(user=user)
        return user
    

class LoginSerializer(serializers.Serializer):
    """
    Handles user logins
    """
    email = serializers.EmailField(required = True)
    password = serializers.CharField(required = True, write_only = True)
    
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)

class PasswordResetConfirmSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only = True, validators = [validate_password])

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only = True)
    new_password = serializers.CharField(write_only = True, validators = [validate_password])


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


# Serializer for the booking model
class BookingSerializer(serializers.ModelSerializer):
    vehicle_name = serializers.CharField(source='vehicle.name', read_only=True)
    vehicle_image = serializers.ImageField(source='vehicle.image', read_only=True)
    daily_rate = serializers.DecimalField(source='vehicle.daily_rate', read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Booking
        fields = [
            'id',
            'user',
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
        read_only_fields = ['id', 'user', 'status', 'vehicle_name', 'vehicle_image', 'daily_rate', 'created_at'] # fields we wouldnt wish the user to edit

    def create(self, validated_data):
        # Aurtomatically calculate total price
        # Total price = vehicle.dailyrate * number of days  
        request = self.context.get('request')
        user = request.user if request else None

        vehicle = validated_data['vehicle']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']

        # validation, end_date must not be before start_date
        if end_date < start_date:
            raise serializers.ValidationError("End date cannot be before start date")
        
        # Calculate number of days
        number_of_days = (end_date - start_date).days + 1

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

