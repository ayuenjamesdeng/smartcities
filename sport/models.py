from django.db import models

# Create your models here.
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