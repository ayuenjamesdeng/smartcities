from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Citizen(models.Model):
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    national_id = models.CharField(max_length=30, unique=True)

class Vehicle(models.Model):
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=30)
    brand = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    manufacture_year = models.IntegerField()

class TrafficSignal(models.Model):
    location = models.CharField(max_length=100)
    signal_status = models.CharField(max_length=20)
    installation_date = models.DateField()
    last_maintenance = models.DateField()

class TransportRoute(models.Model):
    route_name = models.CharField(max_length=100)
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    distance = models.FloatField()
    estimated_time = models.CharField(max_length=30)

class PublicTransport(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    route = models.ForeignKey(TransportRoute, on_delete=models.CASCADE)
    driver_name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    fare = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20)

class ParkingSpace(models.Model):
    space_number = models.CharField(max_length=10)
    floor = models.IntegerField()
    section = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    parking_fee = models.DecimalField(max_digits=8, decimal_places=2)


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    payment_date = models.DateField()
    payment_status = models.CharField(max_length=20)

class Staff(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    position = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

class Calculation(models.Model):
    total_vehicles = models.IntegerField(default=0)
    parked_vehicles = models.IntegerField(default=0)
    exited_vehicles = models.IntegerField(default=0)
    total_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    calculation_date = models.DateTimeField(auto_now=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    citizen = models.OneToOneField(Citizen, on_delete=models.CASCADE, null=True, blank=True, related_name='profile')
    is_first_login = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.citizen.full_name if self.citizen else 'No citizen'}"

class BusLocation(models.Model):
    bus = models.ForeignKey(PublicTransport, on_delete=models.CASCADE, related_name='locations')
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField(default=0)
    heading = models.CharField(max_length=10, blank=True, default='N')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class TransportSchedule(models.Model):
    route = models.ForeignKey(TransportRoute, on_delete=models.CASCADE, related_name='schedules')
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    days_of_week = models.CharField(max_length=100, help_text="Comma-separated: Mon,Tue,Wed,Thu,Fri,Sat,Sun")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.route.route_name} ({self.departure_time} - {self.arrival_time})"

class SmartCard(models.Model):
    card_number = models.CharField(max_length=50, unique=True)
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, null=True, blank=True, related_name='smart_cards')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default='Active')
    issued_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_number} - ${self.balance}"

class Ticket(models.Model):
    ticket_number = models.CharField(max_length=50, unique=True)
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, null=True, blank=True, related_name='tickets')
    route = models.ForeignKey(TransportRoute, on_delete=models.CASCADE, related_name='tickets')
    smart_card = models.ForeignKey(SmartCard, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=30, choices=[
        ('smart_card', 'Smart Card'),
        ('mobile_money', 'Mobile Money'),
        ('cash', 'Cash'),
        ('qr', 'QR Code'),
    ])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    qr_code = models.TextField(blank=True, help_text="Base64 encoded QR data")
    status = models.CharField(max_length=20, default='Active', choices=[
        ('Active', 'Active'),
        ('Used', 'Used'),
        ('Expired', 'Expired'),
        ('Cancelled', 'Cancelled'),
    ])
    purchase_date = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.ticket_number} - {self.route.route_name}"

@receiver(post_save, sender=Citizen)
def create_user_for_citizen(sender, instance, created, **kwargs):
    if created:
        username = instance.national_id
        temp_password = User.objects.make_random_password(length=10)
        user = User.objects.create_user(
            username=username,
            email=instance.email,
            password=temp_password,
            first_name=instance.full_name.split()[0] if instance.full_name else '',
        )
        UserProfile.objects.create(
            user=user,
            citizen=instance,
            is_first_login=True,
        )