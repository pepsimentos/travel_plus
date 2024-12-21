from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F, Q
from .models import Agent, Package, Books, Flight, FlightBooking, Hotel, HotelBooking, PackageFlight, PackageHotel
from django.contrib.auth.models import User

# Helper to check if a user is an agent
def is_agent(user):
    return hasattr(user, 'agent')  # Checks if the user has an associated Agent model

# ================== AUTHENTICATION VIEWS ==================
def homePage(request):
    return render(request, 'users/home.html')

def loginPage(request):
    # If user is already authenticated, redirect to home
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['role'] = 'agent' if is_agent(user) else 'user'
            
            # Get next parameter from URL or default to home
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            
    return render(request, 'users/login.html')

@login_required
def logoutUser(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('home')
    return redirect('home')

def contact_us(request):
    return render(request, 'users/contact_us.html')

@login_required
def home(request):
    return render(request, 'users/home.html')

# ================== PACKAGE VIEWS ==================
def package_details(request, package_id):
    try:
        # Fetch the package details with related data
        package = get_object_or_404(Package, pk=package_id)
        package_flight = PackageFlight.objects.select_related('flight').filter(package=package).first()
        package_hotel = PackageHotel.objects.select_related('hotel').filter(package=package).first()

        # Get availability information
        flight_seats = package_flight.flight.available_seats if package_flight else 0
        hotel_rooms = package_hotel.hotel.available_rooms if package_hotel else 0

        # Get users excluding already booked ones
        booked_users = Books.objects.filter(package=package).values_list('user_id', flat=True)
        available_users = User.objects.exclude(Q(id__in=booked_users) | Q(is_staff=True) | Q(is_superuser=True))

        context = {
            'package': {
                'id': package.package_id,
                'destination': package.pkg_destination,
                'dates': f"{package.pkg_start_date} to {package.pkg_end_date}",
                'price': package.package_price,
                'description': 'Enjoy a premium vacation experience!',
                'flight': f"{package_flight.flight.flight_number} ({flight_seats} seats available)" if package_flight else "No flight available",
                'hotel': f"{package_hotel.hotel.hotel_city} ({hotel_rooms} rooms available)" if package_hotel else "No hotel available",
            },
            'users': available_users if is_agent(request.user) else None,
            'is_agent': is_agent(request.user),
            'has_availability': flight_seats > 0 and hotel_rooms > 0,
        }
        return render(request, 'users/package_details.html', context)
    except Exception as e:
        messages.error(request, f"Error loading package details: {str(e)}")
        return redirect('packages_list')

@login_required
@transaction.atomic
def book_package(request):
    if request.method != 'POST':
        return redirect('packages_list')

    try:
        # Verify agent status
        if not is_agent(request.user):
            messages.error(request, "Only agents can book packages.")
            return redirect('packages_list')

        # Get form data
        package_id = request.POST.get('package_id')
        user_id = request.POST.get('user_id')

        if not package_id or not user_id:
            messages.error(request, "Missing required booking information.")
            return redirect('package_details', package_id=package_id)

        # Get package and user
        package = get_object_or_404(Package, pk=package_id)
        selected_user = get_object_or_404(User, id=user_id)

        # Check if user already has this package
        if Books.objects.filter(user=selected_user, package=package).exists():
            messages.error(request, f"User {selected_user.username} has already booked this package.")
            return redirect('package_details', package_id=package_id)

        # Get associated flight and hotel with select_related for efficiency
        package_flight = PackageFlight.objects.select_related('flight').filter(package=package).first()
        package_hotel = PackageHotel.objects.select_related('hotel').filter(package=package).first()

        if not package_flight or not package_hotel:
            messages.error(request, "Package is missing flight or hotel information.")
            return redirect('package_details', package_id=package_id)

        # Verify availability
        if package_flight.flight.available_seats <= 0:
            messages.error(request, "No flight seats available for this package.")
            return redirect('package_details', package_id=package_id)

        if package_hotel.hotel.available_rooms <= 0:
            messages.error(request, "No hotel rooms available for this package.")
            return redirect('package_details', package_id=package_id)

        # Update capacities
        package_flight.flight.available_seats = F('available_seats') - 1
        package_flight.flight.save()

        package_hotel.hotel.available_rooms = F('available_rooms') - 1
        package_hotel.hotel.save()

        # Create booking
        Books.objects.create(
            user=selected_user,
            agent=request.user.agent,
            package=package
        )

        messages.success(request, f"Package successfully booked for {selected_user.username}!")
        return redirect('success_page')

    except Exception as e:
        messages.error(request, f"An error occurred while booking: {str(e)}")
        return redirect('package_details', package_id=package_id)

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
    try:
        packages = Package.objects.select_related('agent').all()
        
        # Get availability information for each package
        package_info = []
        for package in packages:
            flight = PackageFlight.objects.select_related('flight').filter(package=package).first()
            hotel = PackageHotel.objects.select_related('hotel').filter(package=package).first()
            
            package_info.append({
                'package': package,
                'flight_seats': flight.flight.available_seats if flight else 0,
                'hotel_rooms': hotel.hotel.available_rooms if hotel else 0,
            })

        context = {
            'package_info': package_info,
            'is_agent': is_agent(request.user)
        }
        return render(request, 'users/packages.html', context)
    except Exception as e:
        messages.error(request, f"Error loading packages: {str(e)}")
        return redirect('home')

def hotels_page(request):
    hotels = Hotel.objects.all()[:6]  # Fetch up to 6 hotels from the database
    return render(request, 'users/hotels.html', {'hotels': hotels})