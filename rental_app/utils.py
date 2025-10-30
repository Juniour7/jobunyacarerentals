from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_activation_email(user,uid,token):
    """
    Send email with verification link
    """
    # Ensure you have FRONTEND_URL in your settings.py, e.g., 'http://localhost:3000'
    verification_link = f"{settings.FRONTEND_URL.rstrip('/')}/verify-email/{uid}/{token}"
    subject = "Verify your email address"
    message = (
        f"Hi {user.full_name},\n\n"
        f"Please verify your email by clicking the link below:\n\n"
        f"{verification_link}\n\n"
        "Thank you for registering with Jobunya Car Rentals!"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


def send_password_reset_email(user, uid,token):
    """
    Send a link for password reset
    """
    reset_link = f"{settings.FRONTEND_URL.rstrip('/')}/reset-password/{uid}/{token}"

    subject = "Account Recovery"
    message = (
        f"Hello {user.get_full_name() or user.username},\n\n"
        f"You requested to reset your password.\n\n"
        f"Click the link below to reset it:\n{reset_link}\n\n"
        f"If you didn’t request this, please ignore this email."
    )

    send_mail(
        subject,
        message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )