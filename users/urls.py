from django.urls import path
from . import views  

urlpatterns = [
    path('register/', views.register, name='register'),  # User registration
    path('login/', views.login, name='login'),      # User login
    path('logout/', views.logout, name='logout'),    # User logout
    path('confirm-email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'), 
]