from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, RideEvent, Ride


User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['role'] = user.role
        return token

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        user = User.objects.filter(email=credentials['email']).first()
        if user and user.check_password(credentials['password']):
            data = super().validate(attrs)
            data['email'] = user.email
            data['role'] = user.role
            return data

        raise serializers.ValidationError('Invalid credentials')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id_user', 'role', 'first_name', 'last_name', 'email', 'phone_number']

class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ['id_ride', 'description', 'created_at']


class RideSerializer(serializers.ModelSerializer):
    id_rider = UserSerializer()
    id_driver = UserSerializer()
    todays_ride_events = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    
    class Meta:
        model = Ride
        fields = ['status', 'id_rider', 'id_driver', 'pickup_latitude', 'pickup_longitude',
                  'dropoff_latitude', 'dropoff_longitude', 'pickup_time', 'todays_ride_events','distance']
