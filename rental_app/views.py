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
    ChangePasswordSerializer, VehicleSerializer, BookingSerializer
) 

from .models import Vehicle, Booking, UserProfile

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
        request.user.auth_token.delete()
    except Exception:
        pass
    return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)



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

    Token.objects.filter(user=request.user).delete()

    return Response({'detail' : 'Password changed successfully'})


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



# Vehicle Listing, and creating views
@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def vehicle_list_create_view(request):
    """
    POST: Create vehicles from the dashboard (only admin)
    GET: List vehicles in the front-end
    """
    # handles GET request
    if request.method == 'GET':
        vehicles = Vehicle.objects.all() # fetch all vehicles from the DB
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Handles POST request only admins
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'error' : 'You must be loggen in as admin to add vehicle'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.user.roles != 'admin':
            return Response({'error': 'Only admins can add a vehicle'})
        
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.hHTTP)

    
@api_view(['PUT', 'DELETE', 'GET'])
@permission_classes([AllowAny])
def vehicle_detail_view(request, pk):
    """
    GET    → Retrieve a specific vehicle by ID (public to anyone)
    PUT    → Update a vehicle (admin)
    DELETE → Delete a vehicle (admin)
    """
    try:
        vehicle = Vehicle.objects.get(pk=pk)
    except Vehicle.DoesNotExist:
        return Response({'error' : 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)

    # -----Get (Public)------
    if request.method == 'GET':
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # -------PUT (admin only)
    elif request.method == 'PUT':
        if not request.user.is_authenticated or request.user.roles != 'admin':
            return Response({'error' : 'Only admins can update vehicles'})
        
        serializer = VehicleSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # -----DELETE (admin only)
    elif request.method == 'DELETE':
        if not request.user.is_authenticated or request.user.roles != 'admin':
            return Response({'error' : 'Only admins can delete a vehicle'})
        
        vehicle.delete()
        return Response({'message' : 'Vehice deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

    
# Booking placements views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking_view(request):
    """
    POST: Logged in users can book a vehicle
    """
    if request.user.roles != 'customer':
        return Response({'error' : 'Login to make a booking'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = BookingSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user) # auto-link logged-in-customer
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_bookings(request):
    """
    GET: List all booking made by customer in their dashboard
    """
    bookings = Booking.objects.filter(user=request.user)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def  all_booking_view(request):
    """
    GET: List all booking of all customers in the admin dashboard
    """
    if request.user.roles != 'admin':
        return Response({'error': 'Only Admins can view all bookings'}, status=status.HTTP_403_FORBIDDEN)
    
    bookings = Booking.objects.all().order_by('-created_at')
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_booking_status_view(request, pk):
    """
    PUT:Admin updates the booking status 
    """
    if request.user.roles != 'admin':
        return Response({'error' : 'Only Admin can update booking status'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        booking = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return Response({'error' : 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

    status_value = request.data.get('status')
    if status_value not in ['confirmed',  'cancelled', 'completed']:
        return Response({'error' : 'Invalid status value'}, status=status.HTTP_400_BAD_REQUEST)
    
    booking.status = status_value
    booking.save()

    serializer = BookingSerializer(booking)
    return Response(serializer.data, status=status.HTTP_200_OK)