# Ride Ahead - Ride Booking Application

A Django-based ride booking application that allows users to book rides and drivers to accept them.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Setup Instructions

1. Clone the repository:
```bash

```

2. Create and activate a virtual environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a new file named `requirements.txt` in the project root and add the following:
```
Django>=5.0.0git clone <repository-url>
cd rideahead
django-crispy-forms>=2.0
Pillow>=10.0.0
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

7. Collect static files:
```bash
python manage.py collectstatic
```

## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:8000/
```

## Application Features

- User Registration and Login
- Ride Booking
- Driver Registration
- Ride Management
- Profile Management
- Real-time Ride Status Updates

## Project Structure

```
rideahead/
├── manage.py
├── requirements.txt
├── rideahead/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── rides/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── templates/
│   ├── bunny.html
│   ├── driver_rides.html
│   ├── index.html
│   ├── login.html
│   ├── profile.html
│   ├── register.html
│   ├── rider.html
│   ├── user_ride_details.html
│   └── user_rides.html
└── static/
    └── ...
```

## Usage Guide

1. **User Registration**
   - Click on "Register" to create a new account
   - Fill in the required details
   - Login with your credentials

2. **Booking a Ride**
   - Login to your account
   - Navigate to the booking page
   - Enter pickup and destination locations
   - Select vehicle type and time
   - Confirm booking

3. **Driver Registration**
   - Login to your account
   - Navigate to driver registration
   - Fill in driver details
   - Submit required documents

4. **Managing Rides**
   - View your rides in the dashboard
   - Track ride status
   - View ride details
   - Accept/reject rides (for drivers)

## Troubleshooting

If you encounter any issues:

1. Check if all dependencies are installed:
```bash
pip install -r requirements.txt
```

2. Ensure migrations are up to date:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Clear browser cache if experiencing template issues

4. Check Django server logs for error messages

## Support

For any issues or questions, please contact the development team or create an issue in the repository. 