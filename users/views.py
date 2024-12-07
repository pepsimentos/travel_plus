from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from .models import User, Agent, Package, Books
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, 'users/home.html')

def register(request):
    return render(request, 'users/register.html')

def loginPage(request):

    if request.method == 'POST': #if the user has entered their information, get this info
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist') #if the username does not have any match in the database throw a flash message

        user = authenticate(request, email=email, password=password) #if the user exists chekc if the username and password of the user are correct

        if user is not None: #if the user credentials are correct and the authentication went well authenticate the user
            login(request, user) #add the session into teh database and make sure the user logs in using built in login method of django
            return redirect('home') #after the user logs in redirect them to home
        else:
            messages.error(request, 'email or password does not exist') #throw a flash message if the  credentials aare wrong

    context = {}
    return render(request, 'users/login.html', context)
 
def logoutUser(request):
    logout(request)
    return redirect('home')

def confirm_email(request):
    return render(request, 'users/confirm_email.html')

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


