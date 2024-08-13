
# Ride Management API


## Overview

The Ride Management API allows for the management and tracking of rides, events, and users. It includes features like pagination, filtering, sorting, and role-based access control.

## Setup Instructions

Follow these steps to set up the project on your local machine.

## Setup Instructions

1. Clone the repository.

2. CD rides_project.
    ```bash
    cd rides_project
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Generate Sample Data:
    ```bash
    python manage.py generate_sample_data
    ```
    
7. Run the development server:
    ```bash
    python manage.py runserver
    ```


## API Endpoints

### API Endpoints Authentication and Token Generation

- `POST /token/` - Generate new Token based on username and password
    
    {
        "username": "your_username",
        "password": "your_password"
    }

  
- `POST token/refresh/` - Generate new Token based on refresh token
    
    {
        "refresh": "your_refresh_token"
    }


### API Endpoints Rides

- `GET /rides/` - List of rides with pagination, filtering, and sorting.
- `GET /rides/?ordering=distance&latitude=<LATITUDE VALUE>&longitude=<LONGITUDE VALUE>` - Sort by Distance
- `GET /rides/?ordering=-pickup_time` - Sort by Pickup Time
- `GET /rides/?email=user8@example.com` - Filter by Email
- `GET /rides/?status=pickup` - Filter by Status
- `POST /rides/` - Create a new ride.
- `GET /rides/<id>/` - Retrieve a specific ride.
- `PUT /rides/<id>/` - Update a ride.
- `DELETE /rides/<id>/` - Delete a ride.


### API Endpoints RideEvent

- `GET /ride-events/` - List of rides with pagination, filtering, and sorting.
- `POST /ride-events/` - Create a new ride-event.
- `GET /ride-events/<id>/` - Retrieve a specific ride-event.
- `PUT /ride-events/<id>/` - Update a riride-eventde.
- `DELETE /ride-events/<id>/` - Delete a ride-event.


### API Endpoints User

- `GET /users/` - List of rides with pagination, filtering, and sorting.
- `POST /users/` - Create a new user.
- `GET /users/<id>/` - Retrieve a specific user.
- `PUT /users/<id>/` - Update a user.
- `DELETE /users/<id>/` - Delete a user.



## Authentication
Only users with the role `admin` can access the API.



## SQL Query for Reporting

```sql
SELECT
    strftime('%Y-%m', e1.created_at) AS month,
    d.first_name || ' ' || d.last_name AS driver,
    COUNT(*) AS count_of_trips
FROM
    rides_app_ride r
LEFT JOIN rides_app_rideevent e1 ON r.id_ride = e1.id_ride and e1.description = 'Status changed to pickup'
LEFT JOIN rides_app_rideevent e2 ON r.id_ride = e2.id_ride AND e2.description = 'Status changed to dropoff'
JOIN rides_app_user d ON r.id_user_driver = d.id_user
WHERE
    e1.id_ride IS NOT NULL
    AND e2.id_ride IS NOT NULL
    AND strftime('%s', e2.created_at) - strftime('%s', e1.created_at) > 3600
GROUP BY
    month, driver
ORDER BY
    month, driver;

