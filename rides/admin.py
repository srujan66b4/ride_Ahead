from django.contrib import admin
from .models import Rider, Ride

@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'ride_type', 'is_verified', 'created_at')
    list_filter = ('ride_type', 'is_verified')
    search_fields = ('user__username', 'phone', 'pan_number', 'license_number')

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('rider', 'pickup_location', 'destination', 'scheduled_time', 'status')
    list_filter = ('status', 'scheduled_time')
    search_fields = ('rider__user__username', 'pickup_location', 'destination')
