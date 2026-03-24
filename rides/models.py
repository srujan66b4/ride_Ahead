from django.db import models
from django.contrib.auth.models import User

# Force model changes
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Rider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    pan_number = models.CharField(max_length=10)
    license_number = models.CharField(max_length=20)
    aadhaar_number = models.CharField(max_length=12)
    ride_type = models.CharField(max_length=10, choices=[
        ('bike', 'Bike'),
        ('car', 'Car'),
        ('auto', 'Auto')
    ])
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.ride_type}"

class Ride(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides')
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE, null=True, blank=True, related_name='assigned_rides')
    pickup_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    scheduled_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ride from {self.pickup_location} to {self.destination}"
