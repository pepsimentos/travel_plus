from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from .models import User, Agent, Package, Books

def home(request):
    return render(request, 'users/home.html')

def register(request):
    return render(request, 'users/register.html')

def login(request):
    return render(request, 'users/login.html')
 
def confirm_email(request):
    return render(request, 'users/confirm_email.html')

def logout(request):
    return render(request, 'users/logout.html')

def book_vacation_package(request):
    if request.method == 'POST':
        # Ensure the user is authenticated and is an agent
        if not request.user.is_authenticated or not request.user.is_staff:  # Assuming agents are staff
            return HttpResponseForbidden("You do not have permission to book a package.")

        # Extract form data (or request data)
        user_id = request.POST.get('user_id')  # Replace with request.data.get('user_id') for API
        agent_id = request.POST.get('agent_id')
        package_id = request.POST.get('package_id')

        # Validate that the user, agent, and package exist
        user = get_object_or_404(User, user_id=user_id)
        agent = get_object_or_404(Agent, agent_id=agent_id)
        package = get_object_or_404(Package, package_id=package_id)

        # Create a booking
        try:
            booking = Books.objects.create(user=user, agent=agent, package=package)
            return JsonResponse({'success': True, 'message': 'Package booked successfully!', 'booking_id': booking.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'bookings/book_package.html') # Render the booking form for GET requests


