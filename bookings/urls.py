from django.urls import path
from . import views

urlpatterns = [
    # 0th Page (Landing)
    path('', views.index, name='index'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Booking & Search
    path('search/', views.search_page, name='search_page'),
    path('results/', views.search_results, name='search_results'),
    path('book/<int:bus_id>/', views.book_ticket, name='book_ticket'),
    path('success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('cancel/<int:booking_id>/', views.cancel_ticket, name='cancel_ticket'),
    
    # My Bookings (New)
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]