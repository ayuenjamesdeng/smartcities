from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import time, timedelta
from sport.models import (
    Citizen, Vehicle, TrafficSignal, TransportRoute, PublicTransport,
    ParkingSpace, Payment, Staff, Calculation, TransportSchedule,
    BusLocation, SmartCard, Ticket, UserProfile,
)


class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **options):
        TransportSchedule.objects.all().delete()
        BusLocation.objects.all().delete()
        SmartCard.objects.all().delete()
        Ticket.objects.all().delete()
        Calculation.objects.all().delete()
        Staff.objects.all().delete()
        Payment.objects.all().delete()
        ParkingSpace.objects.all().delete()
        PublicTransport.objects.all().delete()
        Vehicle.objects.all().delete()
        TrafficSignal.objects.all().delete()
        TransportRoute.objects.all().delete()
        UserProfile.objects.all().delete()
        Citizen.objects.filter(national_id__startswith='NID').delete()
        User.objects.filter(username__startswith='NID').delete()

        c1 = Citizen.objects.create(full_name='John Mwangi', gender='Male', phone='0711000001', email='john@mail.com', address='Nairobi CBD', national_id='NID001001')
        c2 = Citizen.objects.create(full_name='Mary Wanjiku', gender='Female', phone='0722000002', email='mary@mail.com', address='Mombasa Road', national_id='NID002002')
        c3 = Citizen.objects.create(full_name='Peter Kamau', gender='Male', phone='0733000003', email='peter@mail.com', address='Kisumu', national_id='NID003003')

        route1 = TransportRoute.objects.create(route_name='Route A: CBD - Eastlands', start_point='CBD', end_point='Eastlands', distance=12.5, estimated_time='35 min')
        route2 = TransportRoute.objects.create(route_name='Route B: CBD - Westlands', start_point='CBD', end_point='Westlands', distance=8.3, estimated_time='25 min')
        route3 = TransportRoute.objects.create(route_name='Route C: CBD - Airport', start_point='CBD', end_point='JKIA', distance=18.0, estimated_time='45 min')

        v1 = Vehicle.objects.create(citizen=c1, plate_number='KCA 001A', vehicle_type='Car', brand='Toyota', color='White', manufacture_year=2022)
        v2 = Vehicle.objects.create(citizen=c2, plate_number='KCB 002B', vehicle_type='Motorcycle', brand='Honda', color='Red', manufacture_year=2023)
        v3 = Vehicle.objects.create(citizen=c3, plate_number='KCC 003C', vehicle_type='Car', brand='Nissan', color='Blue', manufacture_year=2021)

        sig1 = TrafficSignal.objects.create(location='CBD Junction', signal_status='Active', installation_date='2023-01-15', last_maintenance='2024-06-01')
        sig2 = TrafficSignal.objects.create(location='Moi Avenue', signal_status='Active', installation_date='2023-03-20', last_maintenance='2024-05-15')
        sig3 = TrafficSignal.objects.create(location='Uhuru Highway', signal_status='Maintenance', installation_date='2022-11-01', last_maintenance='2024-07-01')
        sig4 = TrafficSignal.objects.create(location='Airport Road', signal_status='Active', installation_date='2024-01-10', last_maintenance='2024-08-01')

        pub1 = PublicTransport.objects.create(vehicle=v1, route=route1, driver_name='James Ochieng', capacity=40, fare=150.00, status='Active')
        pub2 = PublicTransport.objects.create(vehicle=v2, route=route2, driver_name='Sarah Nyambura', capacity=30, fare=100.00, status='Active')
        pub3 = PublicTransport.objects.create(vehicle=v3, route=route3, driver_name='David Kiplagat', capacity=50, fare=250.00, status='Active')

        ParkingSpace.objects.create(space_number='A01', floor=1, section='A', status='Available', parking_fee=50.00)
        ParkingSpace.objects.create(space_number='A02', floor=1, section='A', status='Occupied', parking_fee=50.00)
        ParkingSpace.objects.create(space_number='B01', floor=2, section='B', status='Available', parking_fee=40.00)

        Payment.objects.create(amount=150.00, payment_method='Mobile Money', payment_date='2024-07-15', payment_status='Completed')
        Payment.objects.create(amount=250.00, payment_method='Card', payment_date='2024-07-16', payment_status='Completed')

        Staff.objects.create(first_name='Admin', last_name='User', phone='0700000000', email='admin@smartcity.com', position='System Administrator', salary=150000.00)
        Staff.objects.create(first_name='Jane', last_name='Doe', phone='0711111111', email='jane@smartcity.com', position='Traffic Officer', salary=80000.00)

        Calculation.objects.create(total_vehicles=150, parked_vehicles=80, exited_vehicles=70, total_hours=420.5, total_amount=12500.00)

        now = timezone.now()
        TransportSchedule.objects.create(route=route1, departure_time=time(6, 0), arrival_time=time(6, 35), days_of_week='Mon,Tue,Wed,Thu,Fri', is_active=True)
        TransportSchedule.objects.create(route=route1, departure_time=time(7, 0), arrival_time=time(7, 35), days_of_week='Mon,Tue,Wed,Thu,Fri,Sat', is_active=True)
        TransportSchedule.objects.create(route=route1, departure_time=time(17, 0), arrival_time=time(17, 35), days_of_week='Mon,Tue,Wed,Thu,Fri', is_active=True)
        TransportSchedule.objects.create(route=route2, departure_time=time(6, 30), arrival_time=time(6, 55), days_of_week='Mon,Tue,Wed,Thu,Fri,Sat,Sun', is_active=True)
        TransportSchedule.objects.create(route=route2, departure_time=time(8, 0), arrival_time=time(8, 25), days_of_week='Mon,Tue,Wed,Thu,Fri', is_active=True)
        TransportSchedule.objects.create(route=route3, departure_time=time(5, 0), arrival_time=time(5, 45), days_of_week='Mon,Tue,Wed,Thu,Fri,Sat,Sun', is_active=True)
        TransportSchedule.objects.create(route=route3, departure_time=time(12, 0), arrival_time=time(12, 45), days_of_week='Mon,Tue,Wed,Thu,Fri', is_active=True)

        BusLocation.objects.create(bus=pub1, latitude=-1.286389, longitude=36.817223, speed=45.2, heading='NE', timestamp=now - timedelta(minutes=2))
        BusLocation.objects.create(bus=pub2, latitude=-1.289500, longitude=36.821000, speed=30.0, heading='SW', timestamp=now - timedelta(minutes=1))
        BusLocation.objects.create(bus=pub3, latitude=-1.319000, longitude=36.927000, speed=0, heading='N', timestamp=now - timedelta(minutes=5))

        for citizen in [c1, c2, c3]:
            sc = SmartCard.objects.create(
                card_number=f'SC-{citizen.national_id[-4:]}-{citizen.id}',
                citizen=citizen, balance=500.00, status='Active'
            )
            Ticket.objects.create(
                ticket_number=f'TKT-{now.strftime("%Y%m%d")}-{citizen.id}01',
                citizen=citizen, route=route1, smart_card=sc,
                payment_method='smart_card', amount=150.00,
                qr_code=f'SMARTCITY-TKT-{now.strftime("%Y%m%d")}-{citizen.id}01',
                valid_until=now + timedelta(days=1), status='Active'
            )

        self.stdout.write(self.style.SUCCESS('Sample data seeded successfully!'))
        self.stdout.write(f'Citizens: John (NID001001), Mary (NID002002), Peter (NID003003)')
        self.stdout.write(f'They each have a User account (username = National ID)')
        self.stdout.write(f'Login with National ID and set password on first login')
