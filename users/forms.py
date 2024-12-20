from django import forms
from .models import FlightBooking

class FlightBookingForm(forms.ModelForm):
    class Meta:
        model = FlightBooking
        fields = []  
