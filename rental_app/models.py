from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserProfile(AbstractUser):
    """
    User table extending from Abstractuser to add some extra fields
    """
    ROLES = [
        ('admin', 'admin'),
        ('customer', 'customer'),
    ]
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=10, unique=True)
    roles = models.CharField(max_length=20, choices=ROLES, default='customer')
    agree_terms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} {self.roles}"
    

class Admin(models.Model):
    """
    Admin user profile
    """
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='admin_profile')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return {self.user.username}


class Vehicle(models.Model):
    """
    This is the Vehcile table to stores various vehicles in the database
    """
    TRANSMISSION_CHOICES = [
        ('Automatic', 'Automatic'),
        ('Manual', 'Manual'),
    ]
    FUEL_CHOICES = [
        ('Diesel', 'Diesel'),
        ('Petrol', 'Petrol'),
    ]
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Booked', 'Booked'),
    ]
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    car_type = models.CharField(max_length=200)
    description = models.TextField()
    seats = models.IntegerField()
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    fuel_type = models.CharField(max_length=50, choices=FUEL_CHOICES)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    features = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='vehicles/')
    created_at = models.DateTimeField()


class Booking(models.Model):
    """Booking Model to manage bookings"""
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)



