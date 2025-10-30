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
    message = f"Hi {user.full_name}, \n\nPlease verify your email by clicking this link:\n\n{verification_link}\n\nThank you!"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_siletly=False
    )