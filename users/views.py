from django.shortcuts import render

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