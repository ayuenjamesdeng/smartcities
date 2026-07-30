from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    BusLocation, Calculation, Citizen, Payment, PublicTransport,
    SmartCard, Staff, Ticket, TrafficSignal, TransportRoute,
    TransportSchedule, UserProfile, Vehicle,
)


def home(request):
    return render(request, 'home.html')


def service_view(request):
    return render(request, 'service.html')


def about_view(request):
    return render(request, 'about.html')


def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        try:
            citizen = Citizen.objects.get(national_id=identifier)
            profile = UserProfile.objects.get(citizen=citizen)
            if profile.is_first_login:
                login(request, profile.user)
                return redirect('set_password')
        except (Citizen.DoesNotExist, UserProfile.DoesNotExist):
            pass
        user = authenticate(request, username=identifier, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('dashboard')
            return redirect('user_dashboard')
        return render(request, 'login.html', {'error': 'Invalid national ID or password.'})
    return render(request, 'login.html')


@login_required(login_url='/login/')
def set_password_view(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        return redirect('dashboard')
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')
        if new_password and new_password == confirm and len(new_password) >= 4:
            request.user.set_password(new_password)
            request.user.save()
            profile.is_first_login = False
            profile.save()
            update_session_auth_hash(request, request.user)
            if request.user.is_staff:
                return redirect('dashboard')
            return redirect('user_dashboard')
        return render(request, 'set_password.html', {'error': 'Passwords must match and be at least 4 characters.'})
    return render(request, 'set_password.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/login/')
def dashboard_view(request):
    context = {
        'citizen_count': Citizen.objects.count(),
        'vehicle_count': Vehicle.objects.count(),
        'signal_count': TrafficSignal.objects.count(),
        'route_count': TransportRoute.objects.count(),
        'transport_count': PublicTransport.objects.count(),
        'payment_count': Payment.objects.count(),
        'staff_count': Staff.objects.count(),
        'calculation_count': Calculation.objects.count(),
        'schedule_count': TransportSchedule.objects.count(),
        'ticket_count': Ticket.objects.count(),
        'active_buses': BusLocation.objects.values('bus').distinct().count(),
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='/login/')
def user_dashboard_view(request):
    try:
        profile = request.user.profile
        citizen = profile.citizen
    except (UserProfile.DoesNotExist, AttributeError):
        citizen = None
    if not citizen:
        return redirect('dashboard')
    bus_locations = BusLocation.objects.select_related('bus', 'bus__route')[:20]
    schedules = TransportSchedule.objects.select_related('route').filter(is_active=True)[:10]
    signals = TrafficSignal.objects.all()[:5]
    tickets = Ticket.objects.filter(citizen=citizen).order_by('-purchase_date')[:5]
    smart_cards = SmartCard.objects.filter(citizen=citizen)
    vehicles = Vehicle.objects.filter(citizen=citizen)
    context = {
        'citizen': citizen,
        'bus_locations': bus_locations,
        'schedules': schedules,
        'signals': signals,
        'tickets': tickets,
        'smart_cards': smart_cards,
        'vehicles': vehicles,
    }
    return render(request, 'user_dashboard.html', context)


@login_required(login_url='/login/')
def bus_tracking_view(request):
    now = timezone.now()
    five_min_ago = now - timedelta(minutes=5)
    recent = BusLocation.objects.filter(timestamp__gte=five_min_ago).select_related('bus', 'bus__route').order_by('-timestamp')
    seen = set()
    buses = []
    for loc in recent:
        if loc.bus_id not in seen:
            seen.add(loc.bus_id)
            buses.append(loc)
    all_buses = PublicTransport.objects.filter(status='Active').select_related('vehicle', 'route')
    context = {
        'buses': buses,
        'all_buses': all_buses,
    }
    return render(request, 'bus_tracking.html', context)


@login_required(login_url='/login/')
def bus_locations_json(request):
    five_min_ago = timezone.now() - timedelta(minutes=5)
    recent = BusLocation.objects.filter(timestamp__gte=five_min_ago).select_related('bus', 'bus__route').order_by('-timestamp')
    seen = set()
    data = []
    for loc in recent:
        if loc.bus_id not in seen:
            seen.add(loc.bus_id)
            data.append({
                'id': loc.id,
                'bus_id': loc.bus_id,
                'driver': loc.bus.driver_name,
                'route': loc.bus.route.route_name,
                'lat': loc.latitude,
                'lng': loc.longitude,
                'speed': loc.speed,
                'heading': loc.heading,
                'timestamp': loc.timestamp.isoformat(),
            })
    return JsonResponse(data, safe=False)


@login_required(login_url='/login/')
def trip_planning_view(request):
    routes = TransportRoute.objects.all()
    from_location = request.GET.get('from', '')
    to_location = request.GET.get('to', '')
    date_str = request.GET.get('date', '')
    results = []
    if from_location and to_location:
        results = TransportSchedule.objects.filter(
            is_active=True,
            route__start_point__icontains=from_location,
            route__end_point__icontains=to_location,
        ).select_related('route')[:20]
    elif from_location:
        results = TransportSchedule.objects.filter(
            is_active=True,
            route__start_point__icontains=from_location,
        ).select_related('route')[:20]
    elif to_location:
        results = TransportSchedule.objects.filter(
            is_active=True,
            route__end_point__icontains=to_location,
        ).select_related('route')[:20]
    else:
        results = TransportSchedule.objects.filter(is_active=True).select_related('route')[:20]
    context = {
        'routes': routes,
        'results': results,
        'from_location': from_location,
        'to_location': to_location,
        'date_str': date_str,
    }
    return render(request, 'trip_planning.html', context)


@login_required(login_url='/login/')
def ticketing_view(request):
    try:
        citizen = request.user.profile.citizen
    except (UserProfile.DoesNotExist, AttributeError):
        citizen = None
    routes = TransportRoute.objects.all()
    smart_cards = SmartCard.objects.filter(citizen=citizen, status='Active') if citizen else []
    tickets = Ticket.objects.filter(citizen=citizen).order_by('-purchase_date') if citizen else []
    if request.method == 'POST':
        route_id = request.POST.get('route_id')
        payment_method = request.POST.get('payment_method')
        card_id = request.POST.get('smart_card')
        route = get_object_or_404(TransportRoute, id=route_id)
        ticket_number = f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{route.id}"
        amount = 0
        fare = PublicTransport.objects.filter(route=route).first()
        if fare:
            amount = fare.fare
        smart_card = None
        if card_id:
            smart_card = SmartCard.objects.filter(id=card_id, citizen=citizen, status='Active').first()
        ticket = Ticket.objects.create(
            ticket_number=ticket_number,
            citizen=citizen,
            route=route,
            smart_card=smart_card,
            payment_method=payment_method,
            amount=amount,
            qr_code=f"SMARTCITY-{ticket_number}",
            valid_until=timezone.now() + timedelta(days=1),
            status='Active',
        )
        if smart_card and payment_method == 'smart_card' and smart_card.balance >= amount:
            smart_card.balance -= amount
            smart_card.save()
        return redirect('ticketing_success', ticket_id=ticket.id)
    context = {
        'routes': routes,
        'smart_cards': smart_cards,
        'tickets': tickets,
    }
    return render(request, 'ticketing.html', context)


@login_required(login_url='/login/')
def ticketing_success_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'ticketing_success.html', {'ticket': ticket})


def allcitizens(request):
    allcitizens = Citizen.objects.all()
    return render(request, 'allcitizens.html', {'allcitizens': allcitizens})


def citizen_detail(request, id):
    citizen = get_object_or_404(Citizen, id=id)
    return render(request, 'citizen_detail.html', {'citizen': citizen})


def add_citizen(request):
    if request.method == 'POST':
        Citizen.objects.create(
            full_name=request.POST['full_name'],
            gender=request.POST.get('gender', ''),
            phone=request.POST.get('phone', ''),
            email=request.POST.get('email', ''),
            address=request.POST.get('address', ''),
            national_id=request.POST['national_id'],
        )
        return redirect('allcitizens')
    return render(request, 'add_citizen.html')


def allvehicles(request):
    allvehicles = Vehicle.objects.select_related('citizen').all()
    return render(request, 'allvehicle.html', {'allvehicles': allvehicles})


def vehicle_detail(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    return render(request, 'vehicle_detail.html', {'vehicle': vehicle})


def add_vehicle(request):
    if request.method == 'POST':
        citizen_id = request.POST.get('citizen')
        Vehicle.objects.create(
            citizen_id=citizen_id,
            plate_number=request.POST['plate_number'],
            vehicle_type=request.POST.get('vehicle_type', ''),
            brand=request.POST.get('brand', ''),
            color=request.POST.get('color', ''),
            manufacture_year=request.POST.get('manufacture_year', 2020),
        )
        return redirect('allvehicles')
    citizens = Citizen.objects.all()
    return render(request, 'add_vehicle.html', {'citizens': citizens})


def allsignals(request):
    allsignals = TrafficSignal.objects.all()
    return render(request, 'allsignals.html', {'allsignals': allsignals})


def signal_detail(request, id):
    signal = get_object_or_404(TrafficSignal, id=id)
    return render(request, 'signal_details.html', {'signal': signal})


def add_signal(request):
    if request.method == 'POST':
        TrafficSignal.objects.create(
            location=request.POST['location'],
            signal_status=request.POST.get('signal_status', 'Active'),
            installation_date=request.POST.get('installation_date') or '2024-01-01',
            last_maintenance=request.POST.get('last_maintenance') or '2024-01-01',
        )
        return redirect('allsignals')
    return render(request, 'add_signal.html')


def allroutes(request):
    allroutes = TransportRoute.objects.all()
    return render(request, 'allroute.html', {'allroutes': allroutes})


def routes_detail(request, id):
    route = get_object_or_404(TransportRoute, id=id)
    return render(request, 'route_detail.html', {'route': route})


def add_route(request):
    if request.method == 'POST':
        TransportRoute.objects.create(
            route_name=request.POST['route_name'],
            start_point=request.POST['start_point'],
            end_point=request.POST['end_point'],
            distance=request.POST.get('distance', 0),
            estimated_time=request.POST.get('estimated_time', ''),
        )
        return redirect('allroutes')
    return render(request, 'add_route.html')


def alltransport(request):
    alltransport = PublicTransport.objects.select_related('vehicle', 'route').all()
    return render(request, 'alltransport.html', {'alltransport': alltransport})


def transport_detail(request, id):
    transport = get_object_or_404(PublicTransport, id=id)
    return render(request, 'transport_detail.html', {'transport': transport})


def add_transport(request):
    if request.method == 'POST':
        PublicTransport.objects.create(
            vehicle_id=request.POST['vehicle_id'],
            route_id=request.POST['route_id'],
            driver_name=request.POST['driver_name'],
            capacity=request.POST['capacity'],
            fare=request.POST['fare'],
            status=request.POST['status'],
        )
        return redirect('alltransport')
    return render(request, 'add_transport.html')


def allpublictransport(request):
    allpublictransport = PublicTransport.objects.select_related('vehicle', 'route').all()
    return render(request, 'allpublic.html', {'allpublictransport': allpublictransport})


def public_transport_detail(request, id):
    public_transport = get_object_or_404(PublicTransport, id=id)
    return render(request, 'public_detail.html', {'public_transport': public_transport})


def add_public_transport(request):
    if request.method == 'POST':
        PublicTransport.objects.create(
            vehicle_id=request.POST['vehicle_id'],
            route_id=request.POST['route_id'],
            driver_name=request.POST['driver_name'],
            capacity=request.POST['capacity'],
            fare=request.POST['fare'],
            status=request.POST['status'],
        )
        return redirect('allpublictransport')
    return render(request, 'add_transport.html')


def allpayments(request):
    allpayments = Payment.objects.all()
    return render(request, 'allpayment.html', {'allpayments': allpayments})


def payment_detail(request, id):
    payment = get_object_or_404(Payment, id=id)
    return render(request, 'payment_detail.html', {'payment': payment})


def add_payment(request):
    if request.method == 'POST':
        Payment.objects.create(
            amount=request.POST['amount'],
            payment_method=request.POST['payment_method'],
            payment_date=request.POST['payment_date'],
            payment_status=request.POST['payment_status'],
        )
        return redirect('allpayments')
    return render(request, 'add_payment.html')


def allstaff(request):
    allstaff = Staff.objects.all()
    return render(request, 'allstaff.html', {'allstaff': allstaff})


def staff_detail(request, id):
    staff = get_object_or_404(Staff, id=id)
    return render(request, 'staff_details.html', {'staff': staff})


def add_staff(request):
    if request.method == 'POST':
        Staff.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            position=request.POST['position'],
            salary=request.POST['salary'],
        )
        return redirect('allstaff')
    return render(request, 'add_staff.html')


def allcalculations(request):
    allcalculations = Calculation.objects.all()
    return render(request, 'allcalculation.html', {'allcalculations': allcalculations})


def calculation_detail(request, id):
    calculation = get_object_or_404(Calculation, id=id)
    return render(request, 'calculations_details.html', {'calculation': calculation})


def add_calculation(request):
    if request.method == 'POST':
        Calculation.objects.create(
            total_vehicles=request.POST['total_vehicles'],
            parked_vehicles=request.POST['parked_vehicles'],
            exited_vehicles=request.POST['exited_vehicles'],
            total_hours=request.POST['total_hours'],
            total_amount=request.POST['total_amount'],
        )
        return redirect('allcalculations')
    return render(request, 'add_calculations.html')


def all_schedules(request):
    all_schedules = TransportSchedule.objects.select_related('route').all()
    return render(request, 'all_schedules.html', {'all_schedules': all_schedules})


def add_schedule(request):
    if request.method == 'POST':
        TransportSchedule.objects.create(
            route_id=request.POST['route_id'],
            departure_time=request.POST['departure_time'],
            arrival_time=request.POST['arrival_time'],
            days_of_week=request.POST.get('days_of_week', ''),
            is_active=request.POST.get('is_active', 'on') == 'on',
        )
        return redirect('all_schedules')
    routes = TransportRoute.objects.all()
    return render(request, 'add_schedule.html', {'routes': routes})


def all_bus_locations(request):
    locations = BusLocation.objects.select_related('bus', 'bus__route').all()[:100]
    return render(request, 'all_bus_locations.html', {'locations': locations})


def add_bus_location(request):
    if request.method == 'POST':
        BusLocation.objects.create(
            bus_id=request.POST['bus_id'],
            latitude=request.POST['latitude'],
            longitude=request.POST['longitude'],
            speed=request.POST.get('speed', 0),
            heading=request.POST.get('heading', 'N'),
        )
        return redirect('all_bus_locations')
    buses = PublicTransport.objects.filter(status='Active').select_related('vehicle', 'route')
    return render(request, 'add_bus_location.html', {'buses': buses})


def all_tickets(request):
    all_tickets = Ticket.objects.select_related('citizen', 'route', 'smart_card').all().order_by('-purchase_date')
    return render(request, 'all_tickets.html', {'all_tickets': all_tickets})


def all_smart_cards(request):
    all_cards = SmartCard.objects.select_related('citizen').all()
    return render(request, 'all_smart_cards.html', {'all_cards': all_cards})


def add_smart_card(request):
    if request.method == 'POST':
        from django.utils.crypto import get_random_string
        card_number = f"SC-{get_random_string(10).upper()}"
        SmartCard.objects.create(
            card_number=card_number,
            citizen_id=request.POST.get('citizen_id') or None,
            balance=request.POST.get('balance', 0),
            status=request.POST.get('status', 'Active'),
        )
        return redirect('all_smart_cards')
    citizens = Citizen.objects.all()
    return render(request, 'add_smart_card.html', {'citizens': citizens})


def profile_view(request):
    try:
        profile = request.user.profile
        citizen = profile.citizen
    except (UserProfile.DoesNotExist, AttributeError):
        citizen = None
    if not citizen:
        return redirect('dashboard')
    smart_cards = SmartCard.objects.filter(citizen=citizen)
    tickets = Ticket.objects.filter(citizen=citizen).order_by('-purchase_date')
    vehicles = Vehicle.objects.filter(citizen=citizen)
    context = {
        'citizen': citizen,
        'smart_cards': smart_cards,
        'tickets': tickets,
        'vehicles': vehicles,
    }
    return render(request, 'profile.html', context)