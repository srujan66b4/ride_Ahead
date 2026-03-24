from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Rider, Ride
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('bunny')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('bunny')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')

from django.contrib.auth import login

def rider_registration(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to register as a rider.')
        return redirect('login')

    if request.method == 'POST':
        try:
            rider = Rider.objects.get(user=request.user)
            # If rider exists, update the profile with POST data
            rider.phone = request.POST.get('phone')
            rider.pan_number = request.POST.get('pan')
            rider.license_number = request.POST.get('license')
            rider.aadhaar_number = request.POST.get('aadhaar')
            rider.ride_type = request.POST.get('rideType')
            rider.save()
            messages.success(request, 'Your rider profile has been updated successfully!')
            login(request, request.user)  # Ensure user is logged in
            return redirect('driver_rides')
        except Rider.DoesNotExist:
            try:
                rider = Rider.objects.create(
                    user=request.user,
                    phone=request.POST.get('phone'),
                    pan_number=request.POST.get('pan'),
                    license_number=request.POST.get('license'),
                    aadhaar_number=request.POST.get('aadhaar'),
                    ride_type=request.POST.get('rideType')
                )
                messages.success(request, 'Your rider profile has been created successfully!')
                login(request, request.user)  # Ensure user is logged in
                return redirect('driver_rides')
            except Exception as e:
                messages.error(request, f'Error creating rider profile: {str(e)}')
    return render(request, 'rider.html')

def book_ride(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        try:
            scheduled_time = request.POST.get('time')
            if scheduled_time:
                try:
                    scheduled_time = datetime.strptime(scheduled_time, '%Y-%m-%dT%H:%M')
                except ValueError:
                    messages.error(request, 'Invalid date/time format. Please use the correct format.')
                    return render(request, 'bunny.html')
            else:
                scheduled_time = None

            ride = Ride.objects.create(
                user=request.user,
                pickup_location=request.POST.get('location'),
                destination=request.POST.get('destination'),
                scheduled_time=scheduled_time
            )
            messages.success(request, 'Your ride has been booked successfully!')
            return redirect('user_ride_details', ride_id=ride.id)
        except Exception as e:
            messages.error(request, f'Error booking ride: {str(e)}')
            return render(request, 'bunny.html')
    
    # Get recent rides for the user
    recent_rides = Ride.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'bunny.html', {'recent_rides': recent_rides})

def user_ride_details(request, ride_id):
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to view ride details.')
        return redirect('login')

    try:
        ride = Ride.objects.get(id=ride_id, user=request.user)
        driver = ride.rider
        # Debug prints
        print(f"DEBUG: Ride ID: {ride.id}, Rider assigned: {driver is not None}")
        if driver:
            print(f"DEBUG: Rider full name: {driver.full_name}, phone: {driver.phone}")
        else:
            print("DEBUG: No rider assigned to this ride.")
        return render(request, 'user_ride_details.html', {
            'ride': ride,
            'driver': driver,
            'debug_driver': driver  # pass driver for debug in template
        })
    except Ride.DoesNotExist:
        messages.error(request, 'Ride not found.')
        return redirect('bunny')

def user_rides(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to view your rides.')
        return redirect('login')

    rides = Ride.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_rides.html', {
        'rides': rides
    })

@login_required
def ride_confirmation(request):
    return render(request, 'confirmation.html')

@login_required
def thank_you(request):
    return redirect('driver_rides')

def index(request):
    return render(request, 'index.html')

def driver_rides(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to view your rides.')
        return redirect('login')

    try:
        rider = Rider.objects.get(user=request.user)
        # Show both assigned rides and available rides
        assigned_rides = Ride.objects.filter(rider=rider, status__in=['pending', 'accepted'])
        available_rides = Ride.objects.filter(rider__isnull=True, status='pending')
        return render(request, 'driver_rides.html', {
            'assigned_rides': assigned_rides,
            'available_rides': available_rides,
            'rider': rider
        })
    except Rider.DoesNotExist:
        messages.error(request, 'You need to register as a driver first.')
        return redirect('rider_registration')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def accept_ride(request, ride_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        rider = Rider.objects.get(user=request.user)
        ride = Ride.objects.get(id=ride_id, status='pending')
        ride.rider = rider
        ride.status = 'accepted'
        ride.save()
        print(f"DEBUG: Ride {ride_id} accepted by rider {rider.full_name}")
        messages.success(request, 'Ride accepted successfully!')
    except (Rider.DoesNotExist, Ride.DoesNotExist):
        print(f"DEBUG: Failed to accept ride {ride_id} by user {request.user.username}")
        messages.error(request, 'Invalid ride or you are not a registered driver.')
    
    return redirect('driver_rides')

def reject_ride(request, ride_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        rider = Rider.objects.get(user=request.user)
        ride = Ride.objects.get(id=ride_id, status='pending')
        ride.status = 'cancelled'
        ride.save()
        messages.success(request, 'Ride rejected successfully!')
    except (Rider.DoesNotExist, Ride.DoesNotExist):
        messages.error(request, 'Invalid ride or you are not a registered driver.')
    
    return redirect('driver_rides')

def profile(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to view your profile.')
        return redirect('login')
    
    try:
        rider = Rider.objects.get(user=request.user)
        return render(request, 'profile.html', {
            'user': request.user,
            'rider': rider
        })
    except Rider.DoesNotExist:
        return render(request, 'profile.html', {
            'user': request.user,
            'rider': None
        })

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

def driver_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    rider = Rider.objects.get(user=user)
                    # Redirect only if user is a registered driver
                    return redirect('driver_rides')
                except Rider.DoesNotExist:
                    messages.error(request, 'You are not registered as a driver.')
                    return redirect('driver_login')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'driver_login.html', {'form': form})
