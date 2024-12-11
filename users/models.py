from django.db import models
from django.conf import settings  # Import settings to use AUTH_USER_MODEL


# Agent Table
class Agent(models.Model):
    agent_id = models.CharField(primary_key=True, max_length=50)
    agent_first_name = models.CharField(max_length=100, blank=True, null=True)
    agent_last_name = models.CharField(max_length=100, blank=True, null=True)
    agent_phone_nb = models.CharField(max_length=20, blank=True, null=True)
    agent_email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'agent'

    def __str__(self):
        return f"{self.agent_first_name} {self.agent_last_name}"


# Books Table
class Books(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    agent = models.ForeignKey(Agent, on_delete=models.DO_NOTHING)
    package = models.ForeignKey('Package', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'books'
        unique_together = (('user', 'agent', 'package'),)

    def __str__(self):
        return f"{self.user} - {self.agent} - {self.package}"


# Branch Table
class Branch(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.DO_NOTHING, primary_key=True)
    branch_nb = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    branch_phone = models.CharField(max_length=20, blank=True, null=True)
    branch_country = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'branch'

    def __str__(self):
        return f"{self.branch_country} - {self.branch_nb}"


# Flight Table
class Flight(models.Model):
    flight_id = models.CharField(primary_key=True, max_length=50)
    flight_number = models.CharField(max_length=50, blank=True, null=True)
    start_city = models.CharField(max_length=100, blank=True, null=True)
    end_city = models.CharField(max_length=100, blank=True, null=True)
    takeoff_time = models.TimeField(blank=True, null=True)
    landing_time = models.TimeField(blank=True, null=True)
    flight_date = models.DateField(blank=True, null=True)
    flight_class = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'flight'

    def __str__(self):
        return f"{self.flight_number} ({self.start_city} -> {self.end_city})"


# FlightBooking Table
class FlightBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

    class Meta:
        db_table = 'flight_booking'
        unique_together = (('user', 'flight'),)

    def __str__(self):
        return f"{self.user} - {self.flight}"


# Hotel Table
class Hotel(models.Model):
    hotel_id = models.CharField(primary_key=True, max_length=50)
    start_stay = models.DateField(blank=True, null=True)
    end_stay = models.DateField(blank=True, null=True)
    hotel_city = models.CharField(max_length=100, blank=True, null=True)
    room_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'hotel'

    def __str__(self):
        return f"Hotel in {self.hotel_city} ({self.room_type})"


# HotelBooking Table
class HotelBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'hotel_booking'
        unique_together = (('user', 'hotel'),)

    def __str__(self):
        return f"{self.user} - {self.hotel}"


# Package Table
class Package(models.Model):
    package_id = models.CharField(primary_key=True, max_length=50)
    pkg_start_date = models.DateField(blank=True, null=True)
    pkg_end_date = models.DateField(blank=True, null=True)
    package_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pkg_destination = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'package'

    def __str__(self):
        return f"Package to {self.pkg_destination}"


# PackageFlight Table
class PackageFlight(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    class Meta:
        db_table = 'package_flight'
        unique_together = (('flight', 'package'),)

    def __str__(self):
        return f"{self.flight} - {self.package}"


# PackageHotel Table
class PackageHotel(models.Model):
    hotel = models.OneToOneField(Hotel, on_delete=models.DO_NOTHING, primary_key=True)
    package = models.ForeignKey(Package, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'package_hotel'
        unique_together = (('hotel', 'package'),)

    def __str__(self):
        return f"{self.hotel} - {self.package}"
