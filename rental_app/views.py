from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from .serializers import (
    RegisterSerializer, UserSerializer, LoginSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer,
    ChangePasswordSerializer, EmailVerificationSerializer
) 
from .utils import send_activation_email
from .models import  UserProfile





User = get_user_model()


# -----------ENDPOINT FOR REGISTRATIONS--------

# Email Verification
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    """
    POST: Verify user's email using UID and Token.
    Activates the user if valid.
    """
    serializer = EmailVerificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    uidb64 = serializer.validated_data['uid']
    token = serializer.validated_data['token']

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        # Prevent re-using token if already active (optional but good practice)
        if user.is_active:
             return Response({'detail': 'Account is already active, please login.'}, status=status.HTTP_200_OK)

        user.is_active = True
        user.save()
        return Response({'detail': 'Email verified successfully. You can now login.'}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid or expired verification link.'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST']) 
@permission_classes([AllowAny]) 
def register_view(request):
    """
    POST: Register a new user (customer or admin).
    Sets is_active=False and sends a verification email.
    """
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        # Enforcing security ensure its always false
        if user.is_active:
            user.is_active = False
            user.save()

        
        # Generate uid and token for the link
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Send the email through our helper function
        try:
            send_activation_email(user, uid, token)
        except Exception as e:
            return Response(
                {'error' : 'User created but failed to send verification email.', 'details' : str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # 4. Return success WITHOUT auth token
        return Response({
            "detail": "User registered successfully. Please check your email to verify your account."
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_list(request):
    """
    GET: List all users in the admin dashboard
    """
    if request.user.roles != 'admin':
        return Response({'error' : 'Only Admins can view users'}, status=status.HTTP_403_FORBIDDEN)
    
    users = UserProfile.objects.all().order_by('-created_at')
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




# -------- LOGIN --------

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    POST: Login with email and password
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    password = serializer.validated_data['password']

    # Find user by email
    user = User.objects.filter(email__iexact=email).first()

    if not user or not user.check_password(password):
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    if not user.is_active:
        return Response(
            {'detail' : 'Please verify your email address before logging in.'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Create/get token
    token, _ = Token.objects.get_or_create(user=user)
    data = UserSerializer(user).data
    data['token'] = token.key
    return Response(data)


# views.py

@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification_email_view(request):
    """
    POST: Resend verification email if user is inactive.
    Body: { "email": "user@example.com" }
    """
    email = request.data.get('email')
    if not email:
        return Response({'detail': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email__iexact=email)
        
        # Only send if they are NOT yet active
        if not user.is_active:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            send_activation_email(user, uid, token)

        # Generic response to prevent email enumeration
        return Response({'detail': 'If an inactive account exists with this email, a new verification link has been sent.'}, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
         # Same generic response
         return Response({'detail': 'If an inactive account exists with this email, a new verification link has been sent.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    POST: Logout by deleting the token for the current user
    """
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({"detail": "No active session found."}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """
        GET: Retrieve basic user profile for the currently authenticated user
    """
    return Response(UserSerializer(request.user).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    POST: change password for authenticated user
    """
    serializer = ChangePasswordSerializer(data=request.data) # laod the data from the serializer
    serializer.is_valid(raise_exception=True) # validate the data from the serializer
    old_password = serializer.validated_data['old_password']
    new_password = serializer.validated_data['new_password']

    if not request.user.check_password(old_password):
        return Response({'old_password' : 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
    
    request.user.set_password(new_password)
    request.user.save()

    Token.objects.filter(user=request.user).delete() # delete old token

    # create new token
    token = Token.objects.create(user=request.user)

    data = {
        "detail" : "Password changed successfully",
        "toke" : token.key
    }

    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request_view(request):
    """
    POST: request a password reset. Body: { "email": "user@example.com" }
    Sends an email containing uid & token. For dev we use console backend.
    Always returns the same success message to avoid account enumeration.
    """
    serializer = PasswordResetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        # do not reveal whether email exists
        return Response({'detail': 'If an account with that email exists, we will send reset instructions.'}, status=status.HTTP_200_OK)

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    # build a frontend link for user to use
    reset_link = f"{settings.FRONTEND_URL.rstrip('/')}/reset-password/{uid}/{token}"
    subject = "Password reset for your account"
    message = f"Use this link to reset your password:\n\n{reset_link}\n\nIf you did not request a reset, ignore this message."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    return Response({'detail': 'If an account with that email exists, we will send reset instructions.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm_view(request):
    """
    POST: confirm password reset.
    Body: { "uid": "...", "token": "...", "new_password": "..." }
    """
    serializer = PasswordResetConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    uidb64 = serializer.validated_data['uid']
    token = serializer.validated_data['token']
    new_password = serializer.validated_data['new_password']

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    # Invalidate existing tokens so old clients cannot use old tokens
    Token.objects.filter(user=user).delete()

    return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)



