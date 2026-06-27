from django.db import models
from django.contrib.auth.models import User

# Profile model to store extra "stuffs" (phone, etc.)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Profile for {self.user.username}"

class Bus(models.Model):
    bus_number = models.CharField(max_length=20)
    bus_type = models.CharField(max_length=50)  # e.g., Sleeper, AC Seater
    capacity = models.IntegerField()
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()

    def __str__(self):
        return f"{self.bus_number} ({self.origin} to {self.destination})"


class Booking(models.Model):
    # Linking booking to a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=100)
    seats_booked = models.IntegerField(default=1) 
    seat_number = models.IntegerField(null=True, blank=True) 
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.passenger_name} - {self.bus.bus_number}"


class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.origin} to {self.destination}"
