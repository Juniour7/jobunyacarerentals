import django_filters

from .models import Vehicle


class VehicleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    model = django_filters.CharFilter(lookup_expr='icontains')
    car_type = django_filters.CharFilter(lookup_expr='icontains')
    transmission = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.CharFilter(lookup_expr='icontains')
    min_rate = django_filters.NumberFilter(field_name='daily_rate', lookup_expr='gte')
    max_rate = django_filters.NumberFilter(field_name='daily_rate', lookup_expr='lte')
    min_seats = django_filters.NumberFilter(field_name='seats', lookup_expr='gte')
    max_seats = django_filters.NumberFilter(field_name='seats', lookup_expr='lte')

    class Meta:
        model = Vehicle
        fields = [
            'name',
            'model',
            'car_type',
            'transmission',
            'fuel_type',
            'status',
        ]
