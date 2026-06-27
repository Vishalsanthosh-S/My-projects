from django.contrib import admin
from .models import Bus, Route, Booking, UserProfile

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'bus_type', 'origin', 'destination', 'capacity', 'departure_time')
    list_filter = ('origin', 'destination')
    search_fields = ('bus_number', 'origin', 'destination')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('passenger_name', 'bus', 'seats_booked', 'booking_date', 'user')
    list_filter = ('booking_date', 'bus')
    search_fields = ('passenger_name', 'bus__bus_number')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone_number')
    search_fields = ('user__username', 'email')

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'distance')