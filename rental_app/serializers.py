from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password # for password validations
from datetime import timedelta

# Models
from .models import Admin, UserProfile

user = get_user_model()

# Serializers for User profile models
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        # fields to expose
        fields = ['id', 'email', 'full_name', 'phone_number', 'license_number', 'roles', 'agree_terms', 'created_at' ]
        read_only_fields = ['id', 'created_at']
    
class EmailVerificationSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

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

        # Role to customer for all API registrations
        validated_data['roles'] = 'customer'

        user = UserProfile(**validated_data)
        user.set_password(raw_password)
        user.save()
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






