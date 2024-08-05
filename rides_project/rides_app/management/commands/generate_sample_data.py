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

        last_index_user = 0
        while User.objects.filter(email=f'user{last_index_user}@example.com').exists():
            last_index_user+=1

        for i in range(10):
            index_user = i + last_index_user
            role = random.choice(roles)
            User.objects.create_user(
                email=f'user{index_user}@example.com',
                password='password123',
                first_name=f'First{index_user}',
                last_name=f'Last{index_user}',
                role=role,
                phone_number=f'12345678{index_user}'
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
        rides = Ride.objects.all()
        for ride in rides:
            pickup_time = ride.pickup_time
            dropoff_time = pickup_time + timedelta(hours=random.randint(1, 6))

            ride_events = RideEvent.objects.filter(id_ride=ride)

            if len(ride_events) == 0:
                # Create both pickup and dropoff events
                RideEvent.objects.bulk_create([
                    RideEvent(
                        id_ride=ride,
                        description='Status changed to pickup',
                        created_at=pickup_time
                    ),
                    RideEvent(
                        id_ride=ride,
                        description='Status changed to dropoff',
                        created_at=dropoff_time
                    )
                ])
            elif len(ride_events) == 1:
                existing_event = ride_events.first()
                if existing_event.description == 'Status changed to pickup':
                    # Create only the dropoff event
                    RideEvent.objects.create(
                        id_ride=ride,
                        description='Status changed to dropoff',
                        created_at=dropoff_time
                    )
                else:
                    # Create only the pickup event
                    RideEvent.objects.create(
                        id_ride=ride,
                        description='Status changed to pickup',
                        created_at=pickup_time
                    )
        self.stdout.write(self.style.SUCCESS('Successfully created ride events.'))
