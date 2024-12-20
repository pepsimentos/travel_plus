from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from .models import Agent, Package, Books, Flight, FlightBooking, Hotel, HotelBooking, PackageFlight, PackageHotel
from django.contrib.auth.models import User

# Helper to check if a user is an agent
def is_agent(user):
    return hasattr(user, 'agent')  # Checks if the user has an associated Agent model

# ================== AUTHENTICATION VIEWS ==================
def homePage(request):
    return render(request, 'users/home.html')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            request.session['role'] = 'agent' if is_agent(user) else 'user'
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def contact_us(request):
    return render(request, 'users/contact_us.html')

@login_required
def home(request):
    return render(request, 'users/home.html')

# ================== PACKAGE VIEWS ==================
#@login_required
def package_details(request, package_id):
    # Fetch the package details
    package = get_object_or_404(Package, pk=package_id)
    flight = PackageFlight.objects.filter(package=package).first()
    hotel = PackageHotel.objects.filter(package=package).first()

    # Determine user role: agent or user
    agents = Agent.objects.all() if not is_agent(request.user) else None
    users = User.objects.all() if is_agent(request.user) else None

    context = {
        'package': {
            'id': package.package_id,
            'slug': package.pkg_destination.lower().replace(' ', '-'),
            'destination': package.pkg_destination,
            'dates': f"{package.pkg_start_date} to {package.pkg_end_date}",
            'price': package.package_price,
            'description': 'Enjoy a premium vacation experience!',
            'flight': flight.flight.flight_number if flight else "No flight available",
            'hotel': hotel.hotel.hotel_city if hotel else "No hotel available",
        },
        'agents': agents,  # List of agents for users to pick
        'users': users,    # List of users for agents to pick
        'is_agent': is_agent(request.user),  # Role check for conditional rendering
    }
    return render(request, 'package_details.html', context)

@login_required
@transaction.atomic
def book_package(request):
    if request.method == 'POST':
        # Check if user is agent
        if not is_agent(request.user):
            messages.error(request, "You do not have permission to book this package.")
            return redirect('home')

        user_id = request.POST.get('user_id')
        package_id = request.POST.get('package_id')

        user = get_object_or_404(User, id=user_id)
        package = get_object_or_404(Package, package_id=package_id)

        # Reduce flight and hotel capacities atomically
        flight = PackageFlight.objects.select_related('flight').filter(package=package).first()
        hotel = PackageHotel.objects.select_related('hotel').filter(package=package).first()

        if flight and flight.flight.available_seats > 0:
            flight.flight.available_seats = F('available_seats') - 1
            flight.flight.save()
        else:
            messages.error(request, "Flight has no available seats.")
            return redirect('package_details', package_id=package_id)

        if hotel and hotel.hotel.available_rooms > 0:
            hotel.hotel.available_rooms = F('available_rooms') - 1
            hotel.hotel.save()
        else:
            messages.error(request, "Hotel has no available rooms.")
            return redirect('package_details', package_id=package_id)

        # Create the booking
        Books.objects.create(user=user, agent=request.user.agent, package=package)
        messages.success(request, "Package booked successfully!")
        return redirect('success_page')
    return redirect('home')

# ================== FLIGHT VIEWS ==================
@login_required
@transaction.atomic
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, flight_id=flight_id)

    if flight.available_seats <= 0:
        messages.error(request, "No seats available.")
        return redirect('list_flights')

    flight.available_seats -= 1
    flight.save()
    FlightBooking.objects.create(user=request.user, flight=flight)
    messages.success(request, f"Flight {flight.flight_number} successfully booked!")
    return redirect('success_page')

@login_required
def list_flights(request):
    destination = request.GET.get('destination')
    start_date = request.GET.get('start_date')

    if not destination or not start_date:
        messages.error(request, "Please provide destination and date.")
        return render(request, 'users/flight_list.html')

    flights = Flight.objects.filter(
        start_city__iexact="Beirut",
        end_city__icontains=destination,
        flight_date=start_date
    )
    return render(request, 'users/flight_list.html', {'flights': flights})

# ================== HOTEL VIEWS ==================
@login_required
@transaction.atomic
def book_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, hotel_id=hotel_id)

    if hotel.available_rooms <= 0:
        messages.error(request, "No rooms available.")
        return redirect('list_hotels')

    hotel.available_rooms -= 1
    hotel.save()
    HotelBooking.objects.create(
        user=request.user,
        hotel=hotel,
        start_date=request.POST.get('start_date'),
        end_date=request.POST.get('end_date')
    )
    messages.success(request, "Hotel room successfully booked!")
    return redirect('success_page')

# ================== OTHER VIEWS ==================
def agents_page(request):
    agents = Agent.objects.all()
    return render(request, 'users/agentspage.html', {'agents': agents})

def success_page(request):
    return render(request, "users/success.html")

def registerPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
            return redirect('register')

    return render(request, 'users/register.html')

def packages_list(request):
    packages = Package.objects.all()
    context = {
        'packages': packages
    }
    return render(request, 'users/packages.html', context)  # Specify 'users/packages.html'

def hotels_page(request):
    hotels = Hotel.objects.all()[:6]  # Fetch up to 6 hotels from the database
    return render(request, 'users/hotels.html', {'hotels': hotels})

