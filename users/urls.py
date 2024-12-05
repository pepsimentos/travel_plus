from django.urls import path
from . import views  

urlpatterns = [
    path('register/', views.register, name='register'),  # User registration
    path('login/', views.loginPage, name='login'),      # User login
    path('logout/', views.logoutUser, name='logout'),    # User logout
    path('confirm-email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
    path('bookings/book_package/', views.book_vacation_package,name='book_vacation_package'),  # Booking URL
]
