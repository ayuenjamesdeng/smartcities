from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    Calculation,
    Citizen,
    Payment,
    PublicTransport,
    Staff,
    TrafficSignal,
    TransportRoute,
    Vehicle,
)


def home(request):
    return render(request, 'home.html')


def service_view(request):
    return render(request, 'service.html')


def about_view(request):
    return render(request, 'about.html')


def login_view(request):
    if request.method == 'POST':
        return redirect('dashboard')
    return render(request, 'login.html')


def dashboard_view(request):
    return render(request, 'dashboard.html')


def allcitizens(request):
    allcitizens = Citizen.objects.all()
    return render(request, 'allcitizens.html', {'allcitizens': allcitizens})


def citizen_detail(request, id):
    citizen = get_object_or_404(Citizen, id=id)
    return render(request, 'citizen_detail.html', {'citizen': citizen})


def add_citizen(request):
    return render(request, 'add_citizen.html')


def allvehicles(request):
    allvehicles = Vehicle.objects.select_related('citizen').all()
    return render(request, 'allvehicle.html', {'allvehicles': allvehicles})


def vehicle_detail(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    return render(request, 'vehicle_detail.html', {'vehicle': vehicle})


def add_vehicle(request):
    return render(request, 'add_vehicle.html')


def allsignals(request):
    allsignals = TrafficSignal.objects.all()
    return render(request, 'allsignals.html', {'allsignals': allsignals})


def signal_detail(request, id):
    signal = get_object_or_404(TrafficSignal, id=id)
    return render(request, 'signal_details.html', {'signal': signal})


def add_signal(request):
    return render(request, 'add_signal.html')


def allroutes(request):
    allroutes = TransportRoute.objects.all()
    return render(request, 'allroute.html', {'allroutes': allroutes})


def routes_detail(request, id):
    route = get_object_or_404(TransportRoute, id=id)
    return render(request, 'route_detail.html', {'route': route})


def add_route(request):
    return render(request, 'add_route.html')


def alltransport(request):
    alltransport = PublicTransport.objects.select_related('vehicle', 'route').all()
    return render(request, 'alltransport.html', {'alltransport': alltransport})


def transport_detail(request, id):
    transport = get_object_or_404(PublicTransport, id=id)
    return render(request, 'transport_detail.html', {'transport': transport})


def add_transport(request):
    return render(request, 'add_transport.html')


def allpublictransport(request):
    allpublictransport = PublicTransport.objects.select_related('vehicle', 'route').all()
    return render(request, 'allpublic.html', {'allpublictransport': allpublictransport})


def public_transport_detail(request, id):
    public_transport = get_object_or_404(PublicTransport, id=id)
    return render(request, 'public_detail.html', {'public_transport': public_transport})


def add_public_transport(request):
    return render(request, 'add_transport.html')


def allpayments(request):
    allpayments = Payment.objects.all()
    return render(request, 'allpayment.html', {'allpayments': allpayments})


def payment_detail(request, id):
    payment = get_object_or_404(Payment, id=id)
    return render(request, 'payment_detail.html', {'payment': payment})


def add_payment(request):
    return render(request, 'add_payment.html')


def allstaff(request):
    allstaff = Staff.objects.all()
    return render(request, 'allstaff.html', {'allstaff': allstaff})


def staff_detail(request, id):
    staff = get_object_or_404(Staff, id=id)
    return render(request, 'staff_details.html', {'staff': staff})


def add_staff(request):
    return render(request, 'add_staff.html')


def allcalculations(request):
    allcalculations = Calculation.objects.all()
    return render(request, 'allcalculation.html', {'allcalculations': allcalculations})


def calculation_detail(request, id):
    calculation = get_object_or_404(Calculation, id=id)
    return render(request, 'calculations_details.html', {'calculation': calculation})


def add_calculation(request):
    return render(request, 'add_calculations.html')

