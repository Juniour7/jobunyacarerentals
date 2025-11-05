# utils.py
import requests
from django.conf import settings

EMAIL_SERVICE_URL = "https://jobunya-mail.onrender.com/send-email"  # Flask microservice endpoint

def send_activation_email(user, uid, token):
    """Send account activation email through external Flask email service."""
    verification_link = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"

    subject = "Verify Your Jobunya Account"
    body = f"""
    <h2>Welcome to Jobunya!</h2>
    <p>Hi {user.first_name},</p>
    <p>Thank you for signing up. Please verify your account by clicking the link below:</p>
    <p><a href="{verification_link}">Verify My Email</a></p>
    <p>If you did not create an account, please ignore this message.</p>
    """

    try:
        response = requests.post(
            EMAIL_SERVICE_URL,
            json={
                "to": user.email,
                "subject": subject,
                "body": body
            },
            timeout=10  # prevents Django from hanging too long
        )
        response.raise_for_status()
    except Exception as e:
        raise Exception(f"Email service failed: {e}")


def send_password_reset_email(user, uid, token):
    """Send password reset email through external Flask email service."""
    reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

    subject = "Reset Your Jobunya Password"
    body = f"""
    <h2>Password Reset Requested</h2>
    <p>Hi {user.first_name},</p>
    <p>Click the link below to reset your password:</p>
    <p><a href="{reset_link}">Reset My Password</a></p>
    <p>If you did not request a reset, you can safely ignore this email.</p>
    """

    try:
        response = requests.post(
            EMAIL_SERVICE_URL,
            json={
                "to": user.email,
                "subject": subject,
                "body": body
            },
            timeout=10
        )
        response.raise_for_status()
    except Exception as e:
        raise Exception(f"Email service failed: {e}")
