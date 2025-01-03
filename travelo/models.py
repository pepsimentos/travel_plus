# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Agent(models.Model):
    agent_id = models.CharField(primary_key=True, max_length=50)
    session = models.ForeignKey('Session', models.DO_NOTHING, blank=True, null=True)
    agent_first_name = models.CharField(max_length=100, blank=True, null=True)
    agent_last_name = models.CharField(max_length=100, blank=True, null=True)
    agent_phone_nb = models.CharField(max_length=20, blank=True, null=True)
    agent_email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'agent'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Books(models.Model):
    user = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)  # The composite primary key (user_id, agent_id, package_id) found, that is not supported. The first column is selected.
    agent = models.ForeignKey(Agent, models.DO_NOTHING)
    package = models.ForeignKey('Package', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'books'
        unique_together = (('user', 'agent', 'package'),)


class Branch(models.Model):
    agent = models.OneToOneField(Agent, models.DO_NOTHING, primary_key=True)
    branch_nb = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    branch_phone = models.CharField(max_length=20, blank=True, null=True)
    branch_country = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branch'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class Flight(models.Model):
    flight_id = models.CharField(primary_key=True, max_length=50)
    flight_nb = models.CharField(max_length=50, blank=True, null=True)
    start_city = models.CharField(max_length=100, blank=True, null=True)
    end_city = models.CharField(max_length=100, blank=True, null=True)
    takeoff_time = models.TimeField(blank=True, null=True)
    landing_time = models.TimeField(blank=True, null=True)
    flight_date = models.DateField(blank=True, null=True)
    class_field = models.CharField(db_column='class', max_length=20, blank=True, null=True)  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'flight'


class FlightBooking(models.Model):
    user = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)  # The composite primary key (user_id, flight_id) found, that is not supported. The first column is selected.
    flight = models.ForeignKey(Flight, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'flight_booking'
        unique_together = (('user', 'flight'),)


class Hotel(models.Model):
    hotel_id = models.CharField(primary_key=True, max_length=50)
    start_stay = models.DateField(blank=True, null=True)
    end_stay = models.DateField(blank=True, null=True)
    hotel_city = models.CharField(max_length=100, blank=True, null=True)
    room_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hotel'


class HotelBooking(models.Model):
    user = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)  # The composite primary key (user_id, hotel_id) found, that is not supported. The first column is selected.
    hotel = models.ForeignKey(Hotel, models.DO_NOTHING)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hotel_booking'
        unique_together = (('user', 'hotel'),)


class Package(models.Model):
    package_id = models.CharField(primary_key=True, max_length=50)
    pkg_start_date = models.DateField(blank=True, null=True)
    pkg_end_date = models.DateField(blank=True, null=True)
    package_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pkg_destination = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package'


class PackageFlight(models.Model):
    flight = models.OneToOneField(Flight, models.DO_NOTHING, primary_key=True)  # The composite primary key (flight_id, package_id) found, that is not supported. The first column is selected.
    package = models.ForeignKey(Package, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'package_flight'
        unique_together = (('flight', 'package'),)


class PackageHotel(models.Model):
    hotel = models.OneToOneField(Hotel, models.DO_NOTHING, primary_key=True)  # The composite primary key (hotel_id, package_id) found, that is not supported. The first column is selected.
    package = models.ForeignKey(Package, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'package_hotel'
        unique_together = (('hotel', 'package'),)


class Session(models.Model):
    session_id = models.CharField(primary_key=True, max_length=50)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    max_time = models.TimeField(blank=True, null=True)
    login_time = models.DateTimeField(blank=True, null=True)
    last_active = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'session'


class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50)
    session = models.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)
    user_first_name = models.CharField(max_length=100, blank=True, null=True)
    user_last_name = models.CharField(max_length=100, blank=True, null=True)
    user_prefix = models.CharField(max_length=10, blank=True, null=True)
    user_passport_nb = models.CharField(max_length=50, blank=True, null=True)
    user_phone_nb = models.CharField(max_length=20, blank=True, null=True)
    user_email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
