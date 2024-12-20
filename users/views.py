from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .models import Agent, Package, Books, Flight, FlightBooking, Hotel, HotelBooking
from django.db import transaction

# Use the custom user model
User = get_user_model()

def homePage(request):
    return render(request, 'users/home.html')  

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'users/login.html')


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')

        # Check if email or username already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        try:
            # Use create_user for proper password hashing
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
        except ValueError as e:
            messages.error(request, f"Registration failed: {str(e)}")
        except Exception as e:
            messages.error(request, 'An unexpected error occurred during registration.')

    return render(request, 'users/register.html')


def success_page(request):
    return render(request, "users/success.html")

@login_required
def home(request):
    return render(request, 'users/home.html')


def confirm_email(request):
    return render(request, 'users/confirm_email.html')


@login_required
def book_vacation_package(request):
    if request.method == 'POST':
        if not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to book a package.")

        user_id = request.POST.get('user_id')
        agent_id = request.POST.get('agent_id')
        package_id = request.POST.get('package_id')

        user = get_object_or_404(User, id=user_id)
        agent = get_object_or_404(Agent, id=agent_id)  # Assuming `id` field in Agent model
        package = get_object_or_404(Package, id=package_id)  # Assuming `id` field in Package model

        try:
            booking = Books.objects.create(user=user, agent=agent, package=package)
            return JsonResponse({
                'success': True,
                'message': 'Package booked successfully!',
                'booking_id': booking.id
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'bookings/book_package.html')


@login_required
@transaction.atomic  # Ensures atomicity (all-or-nothing database operation)
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, flight_id=flight_id)

    # Check for seat availability
    if flight.available_seats <= 0:
        messages.error(request, "Sorry, no seats are available on this flight.")
        return redirect('list_flights')  # Redirect back to the flight list page

    # Create a booking and update seat count
    flight.available_seats -= 1
    flight.save()

    FlightBooking.objects.create(user=request.user, flight=flight)
    messages.success(request, f"You have successfully booked flight {flight.flight_number}!")

    return redirect('success_page')  # Redirect to a success page

# View to list all available flights
def list_flights(request):
    destination = request.GET.get('destination')  # User-selected destination city
    start_date = request.GET.get('start_date')    # Outbound flight date
    one_way = request.GET.get('one_way')          # Checkbox for "One Way"

    # Ensure destination and start date are provided
    if not destination or not start_date:
        return render(request, 'users/flight_list.html', {
            'error': 'Please provide a destination city and outbound date.'
        })

    # Base query: flights from Beirut to the selected city
    flights = Flight.objects.filter(
        start_city__iexact="Beirut",
        end_city__icontains=destination,
        flight_date=start_date
    )

    # Pass the filtered flights to the template
    return render(request, 'users/flight_list.html', {
        'flights': flights,
        'query': destination,
        'start_date': start_date,
        'one_way': one_way
    })


@login_required
@transaction.atomic
def book_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, hotel_id=hotel_id)

    # Check for room availability
    if hotel.available_rooms <= 0:
        messages.error(request, "Sorry, no rooms are available at this hotel.")
        return redirect('list_hotels')  # Redirect back to the hotel list page

    # Create a booking and update room count
    hotel.available_rooms -= 1
    hotel.save()

    HotelBooking.objects.create(
        user=request.user,
        hotel=hotel,
        start_date=request.POST.get('start_date'),
        end_date=request.POST.get('end_date')
    )
    messages.success(request, f"Hotel room successfully booked in {hotel.hotel_city}!")

    return redirect('success_page')

def agents_page(request):
    return render(request, 'users/agentspage.html')