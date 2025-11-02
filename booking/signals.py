from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking, Vehicle

@receiver(post_save, sender=Booking)
def update_vehicle_status(sender, instance: Booking, **kwargs):
    """
    Automatically updates the vehicle status based on booking status.
    """
    vehicle = instance.vehicle

    status = instance.status.lower()

    if status == 'confirmed':
        vehicle.status = 'Booked'
    elif status in ['pending', 'completed', 'cancelled']:
        # Check if other active bookings exist for this vehicle
        other_active_bookings = Booking.objects.filter(
            vehicle=vehicle,
            status__in=['pending', 'confirmed']
        ).exclude(id=instance.id)
        
        if not other_active_bookings.exists():
            vehicle.status = 'Available'

    vehicle.save()
