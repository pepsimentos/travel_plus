from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.homePage, name='home'),  # Home page
    path('login/', views.loginPage, name='login'),  # Login page
    path('logout/', views.logoutUser, name='logout'),  # Logout
    path('accounts/profile/', views.homePage, name='profile'),
    path('accounts/logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),  # Registration
    
    # Package related URLs
    path('packages/', views.packages_list, name='packages_list'),  # List packages
    path('package/<str:package_id>/', views.package_details, name='package_details'),  # Package details
    path('book-package/', views.book_package, name='book_package'),  # NEW: Book package
    
    # Agent related URLs
    path('agents/', views.agents_page, name='agents_page'),  # Agents page
    
    # Flight related URLs
    path('flights/', views.list_flights, name='list_flights'),  # List flights
    path('book-flight/<str:flight_id>/', views.book_flight, name='book_flight'),  # Book flight
    
    # Hotel related URLs
    path('hotels/', views.hotels_page, name='hotels_page'),  # Hotels page
    path('book-hotel/<str:hotel_id>/', views.book_hotel, name='book_hotel'),  # Book hotel
    
    # Other URLs
    path('success/', views.success_page, name='success_page'),  # Success page
    # path('contact-us/', views.contact_us, name='contact_us'),  # Commented contact page
]

# Serving static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")