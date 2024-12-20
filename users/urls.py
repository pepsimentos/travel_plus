from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='home'),  # Home page
    path('login/', views.loginPage, name='login'),  # Login page
    path('logout/', views.logoutUser, name='logout'),  # Logout
    path('register/', views.registerPage, name='register'),  # Registration
    path('packages/', views.packages_list, name='packages_list'),  # List packages
    path('package/<int:package_id>/', views.package_details, name='package_details'),  # Package details
    path('agents/', views.agents_page, name='agents_page'),  # Agents page
    path('success/', views.success_page, name='success_page'),  # Success page
    path('flights/', views.list_flights, name='list_flights'),  # List flights
    path('book-flight/<str:flight_id>/', views.book_flight, name='book_flight'),  # Book flight
    path('book-hotel/<str:hotel_id>/', views.book_hotel, name='book_hotel'),  # Book hotel
    path('hotels/', views.hotels_page, name='hotels_page'),  # Add this line
    # path('contact-us/', views.contact_us, name='contact_us'),
]


# Serving static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
