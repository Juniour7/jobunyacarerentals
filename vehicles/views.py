from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import VehicleSerializer
from .models import Vehicle
from .filters import VehicleFilter


class VehicleListCreateView(generics.ListCreateAPIView):
    """
    GET: List all vehicles (public)
    POST: Add new vehicle (admin only)
    Supports filter, search, ordering, pagination.
    """
    queryset = Vehicle.objects.all().order_by('-created_at')
    serializer_class = VehicleSerializer
    permission_classes = [permissions.AllowAny]

    # Filtering configuration
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = VehicleFilter
    search_fields = ['name', 'model', 'description', 'features', 'car_type']
    ordering_fields = ['daily_rate', 'seats', 'created_at']

    def perform_create(self, serializer):
        """
        Only admins to create a vehicle
        """
        user = self.request.user
        if not user.is_authenticated:
            return Response({'error' : 'You must be loggen in as admin to add vehicle'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.roles != 'admin':
            return Response({'error': 'Only admins can add a vehicle'})
        
        serializer.save()


    
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
    

    
