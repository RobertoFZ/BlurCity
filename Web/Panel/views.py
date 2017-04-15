# -*- coding: utf-8 -*-
import json

from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect

# Create your views here.
from django.template import RequestContext

from Core.Account.models import User
from Core.Cars.models import Car, CarDocument
from Core.Chat.models import Room, Message
from Core.Notifications.models import Notification
from Core.Routes.models import Route, RouteDay, RouteMarker
from Core.Studies.models import Campus
from Core.baseFunctions import basicArguments, canRequestRoute


def panelView(request):
    args = basicArguments(request)
    try:
        session_type = request.session['session_type']
    except KeyError:
        return redirect('/authentication/choice_login_type')

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

        for route in routes:
            created_at = route.create_at

            # VERIFY THE ROUTE EXPIRE DATE
            if abs(datetime.now() - created_at).days > 3:  # THREE DAYS FOR EXPIRE TIME
                try:
                    Notification.objects.get(route_pk=route.pk, user=route.user).delete()
                except Notification.DoesNotExist:
                    print "Not have notifications"

                # SEND EMAIL NOTIFICATION TO USER
                body = u'Hola %s %s \n\n Te informamos que tu ruta creada en la fecha %s ha expirado, ¡Te invitamos a crear una nueva!' % (
                    route.user.first_name, route.user.last_name, created_at)
                email = EmailMessage(u'Vencimiento de ruta de Blur City', body, to=[route.user.email])
                email.send()

                route.delete()

        args['routes'] = Route.objects.filter(user=request.user)
        args['session_type'] = session_type
        return render(request, 'Panel/Driver/Routes/route_list.html', args)
    elif session_type == "passenger":
        routes = Route.objects.all()
        args['routes'] = routes
        args['session_type'] = session_type
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
            return render(request, 'Panel/Driver/Routes/route_view.html', args)
        elif request.method == "GET":
            return render(request, 'Panel/Driver/Routes/route_view.html', args)
    else:
        last_marker = route_markers.last()
        print last_marker.latitude
        print last_marker.longitude
        args['destiny'] = Campus.objects.get(latitude=last_marker.latitude, longitude=last_marker.longitude)
        return render(request, 'Panel/Driver/Routes/route_view.html', args)


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
    markers = json.loads(request.POST['markers_json'])
    for marker in markers:
        route = Route.objects.get(pk=request.POST['routePk'])
        routeMarker = RouteMarker()
        routeMarker.route = route
        routeMarker.position = marker['position']
        routeMarker.latitude = marker['latitud']
        routeMarker.longitude = marker['longitud']
        routeMarker.save()

    return HttpResponse(1)


def updateRouteMarkers(request):
    route = Route.objects.get(pk=request.POST['routePk'])
    RouteMarker.objects.filter(route=route).delete()
    markers = json.loads(request.POST['markers_json'])
    for marker in markers:
        route = Route.objects.get(pk=request.POST['routePk'])
        routeMarker = RouteMarker()
        routeMarker.route = route
        routeMarker.position = marker['position']
        routeMarker.latitude = marker['latitud']
        routeMarker.longitude = marker['longitud']
        routeMarker.save()

    return HttpResponse(1)


def notificationView(request):
    args = basicArguments(request)

    session_type = request.session['session_type']
    args['session_type'] = session_type
    routes = []
    if session_type == "driver":
        notifications = Notification.objects.filter(user=request.user)
        for notification in notifications:
            route = Route.objects.get(pk=notification.route_pk)
            routes.append(route)

        args['notifications'] = notifications
        args['routes'] = routes
        return render(request, 'Panel/notifications.html', args)
    elif session_type == "passenger":
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
        if not canRequestRoute(request.user, route):
            return HttpResponse("3")
        notification = Notification()
        notification.user = route.user
        notification.request_user = request.user.pk
        notification.status = False
        notification.route_pk = route.pk
        notification.save()

        # SEND EMAIL FOR NOTIFY
        body = 'Tienes una nueva solicitud del usuario %s %s' % (request.user.first_name, request.user.last_name)
        email = EmailMessage('Nueva solicitud', body, to=[route.user.email])
        email.send()
        return HttpResponse("1")


def updateNotification(request):
    notification = Notification.objects.get(pk=request.POST['notification_pk'])
    request_user = User.objects.get(pk=notification.request_user)
    if request.POST['status'] == "1":
        notification.status = True
        notification.save()
        # SEND EMAIL FOR NOTIFY
        body = u'¡El usuario %s %s ah aceptado tu solicitud de aventon! \n Dirigete a www.blurcity.com para ponerte en contacto con él' % (
            request.user.first_name, request.user.last_name)
        email = EmailMessage(u'Informacion sobre aventon', body, to=[request_user.email])
        email.send()
        return HttpResponse(1)
    else:
        notification.status = False
        notification.save()
        # SEND EMAIL FOR NOTIFY
        body = u'El usuario %s %s ah rechazado tu solicitud de aventón \n Dirígete a www.blurcity.com para buscar un nuevo aventón' % (
            request.user.first_name, request.user.last_name)
        email = EmailMessage(u'Información sobre aventón', body, to=[request_user.email])
        email.send()
        return HttpResponse(2)


def messageDriverView(request, user_who_request):
    args = basicArguments(request)
    session_type = request.session['session_type']
    args['session_type'] = session_type
    args['user_who_request'] = user_who_request
    try:
        room = Room.objects.get(user=request.user, user_chat_request=user_who_request)
    except:
        room = Room()
        room.user = request.user
        room.user_chat_request = user_who_request
        room.save()
    if request.method == "GET":
        messages = Message.objects.filter(room=room)
        args['messages'] = messages
        return render(request, 'Panel/messages.html', args)
    else:
        message = Message()
        message.room = room
        message.message = request.POST['message']
        message.user_pk = request.POST['user_pk']
        message.save()
        messages = Message.objects.filter(room=room)
        args['messages'] = messages
        url = '/panel/chat_driver/' + user_who_request

        user = User.objects.get(pk=room.user_chat_request)
        # SEND EMAIL FOR NOTIFY
        body = u'Tienes un nuevo mensaje del usuario %s %s: \n\n %s' % (
            request.user.first_name, request.user.last_name, request.POST['message'])
        email = EmailMessage('Nuevo mensaje', body, to=[user.email])
        email.send()

        return HttpResponseRedirect(url)


def messagePassagerView(request, driver_pk):
    args = basicArguments(request)
    user = User.objects.get(pk=driver_pk)
    session_type = request.session['session_type']
    args['session_type'] = session_type
    args['driver_pk'] = driver_pk
    try:
        room = Room.objects.get(user=user, user_chat_request=request.user.pk)
    except:
        room = Room()
        room.user = user
        room.user_chat_request = request.user.pk
        room.save()
    if request.method == "GET":
        messages = Message.objects.filter(room=room)
        args['messages'] = messages
        return render(request, 'Panel/messages.html', args)
    else:
        message = Message()
        message.room = room
        message.message = request.POST['message']
        message.user_pk = request.POST['user_pk']
        message.save()
        messages = Message.objects.filter(room=room)
        args['messages'] = messages
        url = '/panel/chat_passager/' + driver_pk

        user = User.objects.get(pk=driver_pk)
        # SEND EMAIL FOR NOTIFY
        body = u'Tienes un nuevo mensaje del usuario %s %s: \n\n %s' % (
            request.user.first_name, request.user.last_name, request.POST['message'])
        email = EmailMessage('Nuevo mensaje', body, to=[user.email])
        email.send()

        return HttpResponseRedirect(url)
