from django.urls import path
from . import views  
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.registerPage, name='register'),  # Custom registration page
    path('login/', views.loginPage, name='login'),           # Custom login page (optional)
    path('logout/', views.logoutUser, name='logout'),        # Custom logout page (optional)
    path('confirm-email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
    path('bookings/book_package/', views.book_vacation_package, name='book_vacation_package'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")