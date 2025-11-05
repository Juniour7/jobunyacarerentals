from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
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
) # Only keep for password reset
from .models import UserProfile

User = get_user_model()


# ---------- REGISTER ----------
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    POST: Register a new user and return a valid token.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.is_active = True  # activate immediately
        user.save()

        # Delete any old tokens just to be safe
        Token.objects.filter(user=user).delete()

        # Create authentication token
        token = Token.objects.create(user=user)

        return Response({
            "detail": "User registered successfully.",
            "token": token.key,
            "user": UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ---------- LOGIN ----------
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

    user = User.objects.filter(email__iexact=email).first()
    if not user or not user.check_password(password):
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=user)
    data = UserSerializer(user).data
    data['token'] = token.key
    return Response(data, status=status.HTTP_200_OK)


# ---------- LOGOUT ----------
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


# ---------- PROFILE ----------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """
    GET: Retrieve basic user profile for the currently authenticated user
    """
    return Response(UserSerializer(request.user).data)


# ---------- ADMIN: CUSTOMER LIST ----------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_list(request):
    """
    GET: List all users (admin only)
    """
    if request.user.roles != 'admin':
        return Response({'error': 'Only Admins can view users'}, status=status.HTTP_403_FORBIDDEN)

    users = UserProfile.objects.all().order_by('-created_at')
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ---------- CHANGE PASSWORD ----------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    POST: Change password for authenticated user
    """
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    old_password = serializer.validated_data['old_password']
    new_password = serializer.validated_data['new_password']

    if not request.user.check_password(old_password):
        return Response({'old_password': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)

    request.user.set_password(new_password)
    request.user.save()

    # Invalidate old tokens
    Token.objects.filter(user=request.user).delete()

    # Create new token
    token = Token.objects.create(user=request.user)

    data = {
        "detail": "Password changed successfully",
        "token": token.key
    }

    return Response(data, status=status.HTTP_200_OK)


# ---------- PASSWORD RESET ----------
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request_view(request):
    """
    POST: Request a password reset.
    Body: { "email": "user@example.com" }
    Always returns a generic message to prevent email enumeration.
    """
    serializer = PasswordResetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response(
            {'detail': 'If an account with that email exists, reset instructions will be sent.'},
            status=status.HTTP_200_OK
        )

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    

    return Response(
        {'detail': 'If an account with that email exists, reset instructions will be sent.'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm_view(request):
    """
    POST: Confirm password reset.
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

    # Invalidate old tokens
    Token.objects.filter(user=user).delete()

    return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
