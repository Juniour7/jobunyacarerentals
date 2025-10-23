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
    ChangePasswordSerializer
) 

from .models import  UserProfile

User = get_user_model()


# -----------ENDPOINT FOR REGISTRATIONS--------

@api_view(['POST']) 
@permission_classes([AllowAny]) 
def register_view(request):
    """
    POST: Register a new user (customer or admin).
    Returns user data and auth token on success.
    """
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        user.is_active = True  # Activate immediately
        user.save()

        # Create authentication token
        token, _ = Token.objects.get_or_create(user=user)

        data = UserSerializer(user).data
        data['token'] = token.key

        return Response(data, status=status.HTTP_201_CREATED)
    
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

    # Create/get token
    token, _ = Token.objects.get_or_create(user=user)
    data = UserSerializer(user).data
    data['token'] = token.key
    return Response(data)


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



