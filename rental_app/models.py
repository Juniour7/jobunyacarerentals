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
    username = models.CharField(max_length=150, blank=True, null=True, unique=False)
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=10, unique=True)
    roles = models.CharField(max_length=20, choices=ROLES, default='customer')
    agree_terms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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









