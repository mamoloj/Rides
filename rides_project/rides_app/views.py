from rest_framework import viewsets, filters
from .permissions import IsAdminRole
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RideSerializer, UserSerializer, RideEventSerializer, MyTokenObtainPairSerializer
from .models import RideEvent, User, Ride
from .serializers import UserSerializer, RideEventSerializer, RideSerializer
from django.db.models.functions import ACos, Cos, Radians, Sin
from math import radians
from django.db.models import Prefetch, F, Value
from django.utils import timezone
from datetime import timedelta
from django_filters.rest_framework import DjangoFilterBackend


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]

class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminRole]

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['pickup_time', 'distance']
    permission_classes = [IsAdminRole]


    def get_queryset(self):
        today = timezone.now()
        yesterday = today - timedelta(days=1)

        queryset = Ride.objects.select_related('id_rider', 'id_driver').prefetch_related(
            Prefetch('events', queryset=RideEvent.objects.filter(created_at__range=[yesterday, today]), to_attr='todays_ride_events')
        )


        # Filter and annotate only if 'distance' is in ordering
        ordering = self.request.query_params.get('ordering', None)
        if ordering and 'distance' in ordering:
            R = 6371  # Radius of the Earth in kilometers
            latitude = self.request.query_params.get('latitude', None)
            longitude = self.request.query_params.get('longitude', None)

            if latitude is not None and longitude is not None:
                latitude = float(latitude)
                longitude = float(longitude)

                queryset = queryset.annotate(
                    pickup_lat_rad=Radians('pickup_latitude'),
                    pickup_lon_rad=Radians('pickup_longitude'),
                    ref_lat_rad=Value(radians(latitude)),
                    ref_lon_rad=Value(radians(longitude)),
                    distance=ACos(
                        Sin(F('pickup_lat_rad')) * Sin(F('ref_lat_rad')) +
                        Cos(F('pickup_lat_rad')) * Cos(F('ref_lat_rad')) *
                        Cos(F('ref_lon_rad') - F('pickup_lon_rad'))
                    ) * R
                )

        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context