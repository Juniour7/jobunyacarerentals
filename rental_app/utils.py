import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings

# Initialize once for all messages
def get_brevo_api():
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')
    return sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))


def send_brevo_email(to_email, subject, html_content, text_content=None):
    """Generic Brevo email sender"""
    api_instance = get_brevo_api()

    sender = {
        "email": settings.DEFAULT_FROM_EMAIL,
        "name": "Jobunya Car Rentals"
    }

    to = [{"email": to_email}]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        sender=sender,
        subject=subject,
        html_content=html_content or text_content,
        text_content=text_content,
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
        return True
    except ApiException as e:
        print("❌ Error sending Brevo email:", e)
        return False


def send_activation_email(user, uid, token):
    """Send activation / verification email using Brevo API"""
    verification_link = f"{settings.FRONTEND_URL.rstrip('/')}/verify-email/{uid}/{token}"

    subject = "Verify your email address"
    text_content = (
        f"Hi {user.full_name},\n\n"
        f"Please verify your email by clicking the link below:\n{verification_link}\n\n"
        "Thank you for registering with Jobunya Car Rentals!"
    )

    html_content = f"""
    <p>Hi {user.full_name},</p>
    <p>Please verify your email by clicking the link below:</p>
    <p><a href="{verification_link}" target="_blank">{verification_link}</a></p>
    <p>Thank you for registering with <b>Jobunya Car Rentals</b>!</p>
    """

    send_brevo_email(user.email, subject, html_content, text_content)


def send_password_reset_email(user, uid, token):
    """Send password reset email using Brevo API"""
    reset_link = f"{settings.FRONTEND_URL.rstrip('/')}/reset-password/{uid}/{token}"

    subject = "Account Recovery"
    text_content = (
        f"Hello {user.full_name},\n\n"
        f"You requested to reset your password.\n"
        f"Click the link below to reset it:\n{reset_link}\n\n"
        "If you didn’t request this, please ignore this email."
    )

    html_content = f"""
    <p>Hello {user.full_name},</p>
    <p>You requested to reset your password.</p>
    <p><a href="{reset_link}" target="_blank">Reset Password</a></p>
    <p>If you didn’t request this, please ignore this email.</p>
    """

    send_brevo_email(user.email, subject, html_content, text_content)
