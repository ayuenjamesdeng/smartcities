from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.service_view, name='services'),
    path('about/', views.about_view, name='about'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('citizens/', views.allcitizens, name='allcitizens'),
    path('citizens/add/', views.add_citizen, name='add_citizen'),
    path('addcitizen/', views.add_citizen, name='add_citizen_legacy'),
    path('citizens/<int:id>/', views.citizen_detail, name='citizen_detail'),

    path('vehicles/', views.allvehicles, name='allvehicles'),
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path('vehicles/<int:id>/', views.vehicle_detail, name='vehicle_detail'),

    path('signals/', views.allsignals, name='allsignals'),
    path('signals/add/', views.add_signal, name='add_signal'),
    path('signals/<int:id>/', views.signal_detail, name='signal_detail'),

    path('routes/', views.allroutes, name='allroutes'),
    path('routes/add/', views.add_route, name='add_route'),
    path('routes/<int:id>/', views.routes_detail, name='routes_detail'),

    path('transport/', views.alltransport, name='alltransport'),
    path('transport/add/', views.add_transport, name='add_transport'),
    path('addtransport/', views.add_transport, name='add_transport_legacy'),
    path('transport/<int:id>/', views.transport_detail, name='transport_detail'),

    path('public-transport/', views.allpublictransport, name='allpublictransport'),
    path('public-transport/add/', views.add_public_transport, name='add_public_transport'),
    path('public-transport/<int:id>/', views.public_transport_detail, name='public_transport_detail'),

    path('payments/', views.allpayments, name='allpayments'),
    path('payments/add/', views.add_payment, name='add_payment'),
    path('payments/<int:id>/', views.payment_detail, name='payment_detail'),

    path('staff/', views.allstaff, name='allstaff'),
    path('staff/add/', views.add_staff, name='add_staff'),
    path('staff/<int:id>/', views.staff_detail, name='staff_detail'),

    path('calculations/', views.allcalculations, name='allcalculations'),
    path('calculations/add/', views.add_calculation, name='add_calculation'),
    path('calculations/<int:id>/', views.calculation_detail, name='calculation_detail'),
]