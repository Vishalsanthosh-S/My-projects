from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction  # Added transaction
from .models import Bus, Booking, UserProfile

# --- LANDING PAGE ---
def index(request):
    if request.user.is_authenticated:
        return redirect('search_page')
    return render(request, 'bookings/landing.html')

# --- AUTHENTICATION VIEWS ---

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    email = request.POST.get('email')
                    phone = request.POST.get('phone_number')
                    UserProfile.objects.create(user=user, email=email, phone_number=phone)
                
                login(request, user)
                messages.success(request, "Registration successful! Welcome.")
                return redirect('search_page')
            
            except IntegrityError:
                messages.error(request, "This username is already taken.")
                return render(request, 'bookings/register.html', {'form': form})
        else:
            return render(request, 'bookings/register.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'bookings/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Welcome back!")
            return redirect('search_page')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'bookings/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')

# --- BOOKING & SEARCH VIEWS ---

@login_required(login_url='login')
def search_page(request):
    # If the user is on the search page without search params, show empty
    return render(request, 'bookings/bus_list.html')

@login_required(login_url='login')
def search_results(request):
    origin = request.GET.get('origin', '').strip()
    destination = request.GET.get('destination', '').strip()
    buses = []
    if origin and destination:
        buses = Bus.objects.filter(origin__icontains=origin, destination__icontains=destination)
    return render(request, 'bookings/bus_list.html', {'buses': buses})

@login_required(login_url='login')
def book_ticket(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    
    if request.method == 'POST':
        passenger_name = request.POST.get('passenger_name')
        try:
            seats_requested = int(request.POST.get('seats_requested', 0))
        except ValueError:
            seats_requested = 0

        if 0 < seats_requested <= bus.capacity:
            try:
                with transaction.atomic():
                    # Deduct seats and create booking
                    bus.capacity -= seats_requested
                    bus.save()
                    booking = Booking.objects.create(
                        user=request.user,
                        bus=bus,
                        passenger_name=passenger_name,
                        seats_booked=seats_requested
                    )
                messages.success(request, "Ticket booked successfully!")
                return redirect('booking_success', booking_id=booking.id)
            except Exception:
                messages.error(request, "An error occurred during booking. Please try again.")
        else:
            messages.error(request, f"Invalid seat request. Available: {bus.capacity}")
            
    return render(request, 'bookings/book_ticket.html', {'bus': bus})

@login_required(login_url='login')
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'bookings/booking_success.html', {'booking': booking})

@login_required(login_url='login')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required(login_url='login')
def cancel_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.user != request.user:
        messages.error(request, "Unauthorized access.")
        return redirect('search_page')
        
    try:
        with transaction.atomic():
            bus = booking.bus
            bus.capacity += booking.seats_booked
            bus.save()
            booking.delete()
        messages.success(request, "Booking cancelled successfully.")
    except Exception:
        messages.error(request, "Cancellation failed. Please try again.")
        
    return redirect('my_bookings')