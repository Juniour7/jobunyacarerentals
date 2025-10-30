from django.db import models
from django.contrib.auth import get_user_model
from vehicles.models import Vehicle

UserProfile = get_user_model()

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=150)
    address = models.TextField()
    city = models.CharField(max_length=100)



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
    pickup_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='pickup_bookings')
    dropoff_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='dropoff_bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.user.email} for {self.vehicle.name}"


class DamageReport(models.Model):
    STATUS_CHOICES = [
        ('unresolved', 'Unresolved'),
        ('resolved', 'Resolved'),
    ]
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='unresolved')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Damage report for {self.booking.vehicle}"
