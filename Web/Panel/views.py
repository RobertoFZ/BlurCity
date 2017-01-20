from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext

from Core.Cars.models import Car, CarDocument
from Core.Routes.models import Route, RouteDay, RouteMarker
from Core.baseFunctions import basicArguments


def panelView(request):
    args = basicArguments(request)
    session_type = request.session['session_type']

    if session_type == "driver":
        return render(request, 'Panel/Driver/index.html', args)
    elif session_type == "passenger":
        return render(request, 'Panel/Passenger/index.html', args)


def carListView(request):
    args = basicArguments(request)

    cars = Car.objects.filter(user=request.user)
    cars_documents = []

    for car in cars:
        cars_documents.append(CarDocument.objects.get(car=car))

    args['cars'] = cars
    args['cars_documents'] = cars_documents

    return render(request, 'Panel/Driver/car_list.html', args)


def saveRouteService(request):
    origen = request.POST['origen']
    destiny = request.POST['destiny']
    car = request.POST['car']
    sits = request.POST['sits']
    time = request.POST['time']
    days = request.POST.getlist('day[]')

    route = Route()
    route.user = request.user
    route.campus_pk = destiny
    route.car_pk = car
    route.origin= origen
    route.name = request.user.first_name + "-" + "Ruta"
    route.sits = sits
    route.start_time = time
    route.save()

    for current_day in days:
        day = RouteDay()
        day.route = route
        day.day = current_day
        day.save()

    return HttpResponse(route.pk)


def saveRouteDays(request):
    return HttpResponse("1")


def saveRouteMarkers(request):
    route_pk = request.POST['routePk']
    position = request.POST['position']
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']

    route = Route.objects.get(pk=route_pk)
    routeMarker = RouteMarker()
    routeMarker.route = route
    routeMarker.position = position
    routeMarker.latitude = latitude
    routeMarker.longitude = longitude
    routeMarker.save()

    return HttpResponse(1)
