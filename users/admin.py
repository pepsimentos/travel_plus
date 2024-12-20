from django.contrib import admin
from .models import Flight, FlightBooking, Hotel, HotelBooking, Package

# Register Flight model
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'start_city', 'end_city', 'flight_date', 
                    'takeoff_time', 'landing_time', 'available_seats')  # Added available_seats
    search_fields = ('flight_number', 'start_city', 'end_city')
    list_filter = ('flight_date', 'flight_class')

# Register Hotel model
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('hotel_id', 'hotel_city', 'start_stay', 'end_stay', 
                    'room_type', 'available_rooms')  # Added available_rooms
    search_fields = ('hotel_city', 'hotel_id', 'room_type')
    list_filter = ('start_stay', 'end_stay')

# Register FlightBooking model
@admin.register(FlightBooking)
class FlightBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'flight')
    search_fields = ('user__username', 'flight__flight_number')
    list_filter = ('flight__flight_date',)

# Register HotelBooking model
@admin.register(HotelBooking)
class HotelBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel', 'start_date', 'end_date')
    search_fields = ('user__username', 'hotel__hotel_city')
    list_filter = ('start_date', 'end_date')

# Register Package model
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('package_id', 'pkg_destination', 'pkg_start_date', 'pkg_end_date', 'package_price')
    search_fields = ('package_id', 'pkg_destination')
    list_filter = ('pkg_start_date', 'pkg_end_date')
