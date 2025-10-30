from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework import generics, permissions

from .serializers import BookingSerializer, DamageReportSerializer, LocationSerializer
from .models import Booking, DamageReport, Location
from .permissions import IsAdminRole

# Create your views here.

# ----------------LOCATION EDNPOINTS---------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def location_create_view(request):
    """
    Admin creates and save list of locations
    """
    if not request.user.roles == 'admin':
        return Response(
            {'error' : 'Only admins can add a location'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if request.user.roles == 'admin':
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def location_list_view(request):
    """
    Display List Of Location Options
    """
    location = Location.objects.all()
    serializer = LocationSerializer(location, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_location(request, pk):
    """
    Allow Admin to update the whole location or a section of it
    """
    if request.user.roles != 'admin':
        return Response(
            {'error': 'Only Admins can update the locations'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        location = Location.objects.get(pk=pk)
    except Location.DoesNotExist:
        return Response(
            {'error' : 'Location not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = LocationSerializer(location, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def location_delete_view(request,pk):
    """
    Allow admins to delete a specific location
    """
    if request.user.roles != 'admin':
        return Response(
            {'error' : 'Only admins are allowed to delete a location record'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        location = Location.objects.get(pk=pk)
    except Location.DoesNotExist:
        return Response(
            {'error' : 'Location not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    location.delete()
    return Response({'message': 'Location deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# Booking placements 

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


# ---------Damge Report Enpoints-------

class DamageReportView(generics.ListCreateAPIView):
    """
    Lists and creates damage reports for a particular user
    """
    serializer_class = DamageReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Only return reports for bookings owned by the logged in user"""
        return DamageReport.objects.filter(booking__user=self.request.user)
    
    def perform_create(self,serializer):
        """Save a new damage report"""
        serializer.save()


class AdminDamageReportView(generics.ListAPIView):
    """Lists all damage reports from the users"""
    queryset = DamageReport.objects.all().select_related('booking__vehicle', 'booking__user')
    serializer_class = DamageReportSerializer
    permission_classes = [IsAdminRole]


class AdminDamageReportDetailView(generics.RetrieveUpdateAPIView):
    """
    Admin can view or update the status of a damage report.
    """
    queryset = DamageReport.objects.all().select_related('booking', 'booking__vehicle', 'booking__user')
    serializer_class = DamageReportSerializer
    permission_classes = [IsAdminRole]

    def get_serializer(self, *args, **kwargs):
        """
        Override serializer for PATCH (update) requests to only allow updating `status`.
        """
        serializer_class = self.get_serializer_class()
        if self.request.method in ['PATCH', 'PUT']:
            # Only make 'status' writable
            kwargs['partial'] = True
            serializer = serializer_class(*args, **kwargs)
            serializer.fields['booking'].read_only = True
            serializer.fields['description'].read_only = True
            serializer.fields['images'].read_only = True
            serializer.fields['user_details'] = serializer.fields.get('user_details', None)
        else:
            serializer = serializer_class(*args, **kwargs)
        return serializer