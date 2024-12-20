from django.urls import path
from . import views  
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.registerPage, name='register'),  
    path('login/', views.loginPage, name='login'),           
    path('logout/', views.logoutUser, name='logout'),        
    path('confirm-email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
    path('bookings/book_package/', views.book_vacation_package, name='book_vacation_package'),
    path('flights/', views.list_flights, name='list_flights'),
    path('book-flight/<str:flight_id>/', views.book_flight, name='book_flight'),
    path('agents/', views.agents_page, name='agents_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
    