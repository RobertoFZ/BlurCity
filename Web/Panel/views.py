from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext

from Core.Cars.models import Car, CarDocument
from Core.Notifications.models import Notification
from Core.Routes.models import Route, RouteDay, RouteMarker
from Core.Studies.models import Campus
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


def routeListView(request):
    args = basicArguments(request)

    session_type = request.session['session_type']

    if session_type == "driver":
        routes = Route.objects.filter(user=request.user)
        args['routes'] = routes
        return render(request, 'Panel/Driver/Routes/route_list.html', args)
    elif session_type == "passenger":
        routes = Route.objects.all()
        args['routes'] = routes
        return render(request, 'Panel/Driver/Routes/route_list.html', args)


def routeView(request, route_pk):
    args = basicArguments(request)
    route = Route.objects.get(pk=route_pk)
    cars = Car.objects.filter(user=route.user)
    route_days = RouteDay.objects.filter(route=route)
    route_markers = RouteMarker.objects.filter(route=route)
    campus = Campus.objects.all()

    args['user_cars'] = cars
    args['route'] = route
    args['route_days'] = route_days
    args['route_markers'] = route_markers
    args['campus_list'] = campus
    if request.user == route.user:
        args['is_owner'] = True
        if request.method == "POST":
            print("post")
            return render(request, 'Panel/Driver/Routes/route.html', args)
        elif request.method == "GET":
            return render(request, 'Panel/Driver/Routes/route.html', args)
    else:
        last_marker = route_markers.last()
        args['destiny'] = Campus.objects.get(latitude=last_marker.latitude, longitude=last_marker.longitude)
        return render(request, 'Panel/Driver/Routes/route.html', args)


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
    route.origin = origen
    route.name = request.user.first_name + "-" + "Ruta"
    route.sits = sits
    route.start_time = time
    route.save()

    for current_day in days:
        day = RouteDay()
        day.route = route
        day.day = current_day
        day.save()
        print(day.day)

    return HttpResponse(route.pk)


def updateRouteService(request):
    route_pk = request.POST['routePk']
    origen = request.POST['origen']
    destiny = request.POST['destiny']
    car = request.POST['car']
    sits = request.POST['sits']
    time = request.POST['time']
    days = request.POST.getlist('day[]')

    route = Route.objects.get(pk=route_pk)
    route.campus_pk = destiny
    route.car_pk = car
    route.origin = origen
    route.name = request.user.first_name + "-" + "Ruta"
    route.sits = sits
    route.start_time = time
    route.save()
    RouteDay.objects.filter(route=route).delete()

    for current_day in days:
        day = RouteDay()
        day.route = route
        day.day = current_day
        day.save()

    return HttpResponse(route.pk)


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


def updateRouteMarkers(request):
    route_pk = request.POST['routePk']
    position = request.POST['position']
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']

    route = Route.objects.get(pk=route_pk)
    RouteMarker.objects.filter(route=route).delete()
    routeMarker = RouteMarker()
    routeMarker.route = route
    routeMarker.position = position
    routeMarker.latitude = latitude
    routeMarker.longitude = longitude
    routeMarker.save()

    return HttpResponse(1)


def notificationView(request):
    args = basicArguments(request)

    session_type = request.session['session_type']
    args['session_type'] = session_type
    if session_type == "driver":
        notifications = Notification.objects.filter(user=request.user)
        args['notifications'] = notifications
        return render(request, 'Panel/notifications.html', args)
    elif session_type == "passenger":
        routes = []
        notifications = Notification.objects.filter(request_user=request.user.pk)

        for notification in notifications:
            route = Route.objects.get(pk=notification.route_pk)
            routes.append(route)

        args['notifications'] = notifications
        args['routes'] = routes
        return render(request, 'Panel/notifications.html', args)


def makeNotification(request):
    route_pk = request.POST['route_pk']
    route = Route.objects.get(pk=route_pk)

    try:
        Notification.objects.get(route_pk=route_pk, request_user=request.user.pk)
        return HttpResponse("2")
    except Notification.DoesNotExist:
        notification = Notification()
        notification.user = route.user
        notification.request_user = request.user.pk
        notification.status = False
        notification.route_pk = route.pk
        notification.save()
        return HttpResponse("1")


def updateNotification(request):
    notification = Notification.objects.get(pk=request.POST['notification_pk'])
    print(request.POST['status'])
    if request.POST['status'] == "1":
        notification.status = True
        notification.save()
        return HttpResponse(1)
    else:
        notification.status = False
        notification.save()
        return HttpResponse(2)
