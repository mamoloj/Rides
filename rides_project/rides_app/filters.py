import django_filters
from .models import Ride

class RideFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='exact')
    email = django_filters.CharFilter(field_name='id_rider__email', lookup_expr='exact')

    class Meta:
        model = Ride
        fields = ['status', 'id_rider__email']
