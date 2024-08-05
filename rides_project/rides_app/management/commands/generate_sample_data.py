from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from rides_app.models import User, Ride, RideEvent
import random

class Command(BaseCommand):
    help = 'Generate sample data for User, Ride, and RideEvent models.'

    def handle(self, *args, **kwargs):
        self.generate_users()
        self.generate_rides()
        self.generate_ride_events()

    def generate_users(self):
        roles = ['admin', 'user']
        for i in range(10):
            role = random.choice(roles)
            User.objects.create_user(
                email=f'user{i}@example.com',
                password='password123',
                first_name=f'First{i}',
                last_name=f'Last{i}',
                role=role,
                phone_number=f'12345678{i}'
            )
        self.stdout.write(self.style.SUCCESS('Successfully created users.'))

    def generate_rides(self):
        users = list(User.objects.all())
        statuses = ['en-route', 'pickup', 'dropoff']
        for i in range(40):
            Ride.objects.create(
                id_rider=random.choice(users),
                id_driver=random.choice(users),
                status=random.choice(statuses),
                pickup_latitude=random.uniform(-90.0, 90.0),
                pickup_longitude=random.uniform(-180.0, 180.0),
                dropoff_latitude=random.uniform(-90.0, 90.0),
                dropoff_longitude=random.uniform(-180.0, 180.0),
                pickup_time=timezone.now() - timedelta(days=random.randint(0, 30))
            )
        self.stdout.write(self.style.SUCCESS('Successfully created rides.'))

    def generate_ride_events(self):
        rides = list(Ride.objects.all())
        for i in range(100):
            RideEvent.objects.create(
                id_ride=random.choice(rides),
                description=f'Event description {i}'
            )
        self.stdout.write(self.style.SUCCESS('Successfully created ride events.'))
