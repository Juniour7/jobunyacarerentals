from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# ---------------------------
# Custom User Manager
# ---------------------------
class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('roles', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


# ---------------------------
# Custom User Model
# ---------------------------
class UserProfile(AbstractUser):
    """
    User table extending from AbstractUser to add some extra fields
    """
    ROLES = [
        ('admin', 'admin'),
        ('customer', 'customer'),
    ]

    username = models.CharField(max_length=150, blank=True, null=True, unique=False)
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=10, blank=True, null=True)
    roles = models.CharField(max_length=20, choices=ROLES, default='customer')
    agree_terms = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # 👇 Add the custom manager
    objects = UserProfileManager()

    def __str__(self):
        return f"{self.full_name} ({self.roles})"


# ---------------------------
# Admin Profile
# ---------------------------
class Admin(models.Model):
    """
    Admin user profile
    """
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='admin_profile')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.full_name
