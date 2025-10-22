from django.db import models
from django.utils.text import slugify

# Create your models here.
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
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    min_days = models.IntegerField(blank=True, null=True)
    engine = models.CharField(max_length=100, blank=True, null=True)
    engine_torque = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Generate slug from name if it doesn't exist
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Ensure uniqueness
            while Vehicle.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
    

class VehicleImage(models.Model):
    """
    Additional Images for each vehicle
    """
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='vehicles/')
    uploaded_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.vehicle.name}"

