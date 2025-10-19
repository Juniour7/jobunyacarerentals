from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from .serializers import VehicleSerializer
from .models import Vehicle


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
    

    
