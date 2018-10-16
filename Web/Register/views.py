#!/usr/bin/python
# -*- coding: latin-1 -*-

from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from django.utils.datastructures import MultiValueDictKeyError

from Core.Account.models import User
from Core.Cars.models import Car, CarDocument
from Core.Routes.models import Route
from Core.Studies.models import University, Major, Campus
from Core.baseFunctions import basicArguments


def registerUserView(request):
    args = basicArguments(request)
    if request.method == "POST":
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        try:
            register_id = request.POST['register']
        except KeyError:
            register_id = None
        password = request.POST['password']
        message = ""
        if email == "":
            args['error'] = True
            message = u"El correo electrónico es obligatorio"
            args['message'] = message
            return render(
                request,
                'Register/register_user.html',
                args
            )

        if first_name == "":
            args['error'] = True
            message = u"El nombre es obligatorio"
            args['message'] = message
            return render(
                request,
                'Register/register_user.html',
                args
            )

        if last_name == "":
            args['error'] = True
            message = u"El apellido es obligatorio"
            args['message'] = message
            return render(
                request,
                'Register/register_user.html',
                args
            )

        if email == "":
            args['error'] = True
            message = u"El correo electrónico es obligatorio"
            args['message'] = message
            return render(
                request,
                'Register/register_user.html',
                args
            )

        try:
            major = Major.objects.get(id=request.POST['major'])
        except:
            major = None
        university = University.objects.get(pk=request.POST['university'])
        try:
            user = User.objects.get(email=email)
            errors = []
            errors.append(u"Ya existe un usuario con el correo electrónico ingresado")
            args['errors'] = errors
            args['email'] = email
            args['first_name'] = first_name
            args['last_name'] = last_name

            universitys = University.objects.all()
            majors = Major.objects.all()

            args['universitys'] = universitys
            args['majors'] = majors
            return render(
                request,
                'Register/register_user.html',
                args
            )
        except User.DoesNotExist:
            args['created'] = True
            new_user = User()
            new_user.email = email
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.university = university
            if register_id:
                new_user.register = register_id
            new_user.major = major
            new_user.set_password(password)
            new_user.save()

        return render(
            request,
            'Register/register_user.html',
            args
        )
    elif request.method == "GET":
        universitys = University.objects.all()
        majors = Major.objects.all()

        args['universitys'] = universitys
        args['majors'] = majors

        return render(
            request,
            'Register/register_user.html',
            args
        )


def registerCarView(request):
    args = basicArguments(request)

    if request.method == 'POST':
        model = request.POST['model']
        brand = request.POST['brand']
        registration_tag = request.POST['registration_tag']
        color = request.POST['color']
        total_sits = request.POST['total_sits']
        message = ""

        if brand == "":
            message = u"La marca del vehículo es necesaria"
            args['error'] = True
            args['message'] = message
            return render_to_response('Register/register_car.html', args, RequestContext(request))

        if model == "":
            message = u"El modelo del vehículo es necesario"
            args['error'] = True
            args['message'] = message
            return render_to_response('Register/register_car.html', args, RequestContext(request))

        if registration_tag == "":
            message = u"Las placas del vehículo son necesarias"
            args['error'] = True
            args['message'] = message
            return render_to_response('Register/register_car.html', args, RequestContext(request))

        if color == "":
            message = u"El color del vehículo es necesario"
            args['error'] = True
            args['message'] = message
            return render_to_response('Register/register_car.html', args, RequestContext(request))

        if total_sits == "":
            message = u"El número de asientos disponibles es necesario"
            args['error'] = True
            args['message'] = message
            return render_to_response('Register/register_car.html', args, RequestContext(request))

        try:
            insurance_policy = request.FILES['insurance_policy']
            circulation_card = request.FILES['circulation_card']
            licence = request.FILES['licence']
        except:
            message = u"Todos los documentos son necesarios"
            args['error'] = True
            args['message'] = message
            return render_to_response('Register/register_car.html', args, RequestContext(request))

        car_to_register = Car()
        car_to_register.user = request.user
        car_to_register.model = model
        car_to_register.brand = brand
        car_to_register.registration_tag = registration_tag
        car_to_register.color = color
        car_to_register.total_sits = total_sits
        car_to_register.save()

        car_documents = CarDocument()
        car_documents.car = car_to_register
        car_documents.insurance_policy = insurance_policy
        car_documents.circulation_card = circulation_card
        car_documents.licence = licence
        car_documents.save()

        args['car_registered'] = 'correct'
        return render_to_response('Register/register_car.html', args, RequestContext(request))
    elif request.method == 'GET':
        return render_to_response('Register/register_car.html', args, RequestContext(request))


def editCarView(request, car_pk):
    args = basicArguments(request)

    if request.method == 'POST':
        car = Car.objects.get(pk=car_pk)
        car.model = request.POST['model']
        car.brand = request.POST['brand']
        car.registration_tag = request.POST['registration_tag']
        car.color = request.POST['color']
        car.total_sits = request.POST['total_sits']
        car.save()

        car_documents = CarDocument.objects.get(car=car)

        ## FILES
        try:
            insurance_policy = request.FILES['insurance_policy']
            car_documents.insurance_policy.delete()
            car_documents.insurance_policy = insurance_policy
        except MultiValueDictKeyError:
            print('Not insurance policy updated')

        try:
            circulation_car = request.FILES['circulation_card']
            car_documents.circulation_card.delete()
            car_documents.circulation_card = circulation_car
        except MultiValueDictKeyError:
            print('Not circulation car updated')

        try:
            licence = request.FILES['licence']
            car_documents.licence.delete()
            car_documents.licence = licence
        except MultiValueDictKeyError:
            print('Not licence updated')

        car_documents.save()

        args['car'] = car
        args['car_documents'] = car_documents
        args['car_updated'] = 'correct'

        return render(request, 'Edit/edit_car.html', args)
    elif request.method == 'GET':
        car = Car.objects.get(pk=car_pk)
        car_documents = CarDocument.objects.get(car=car)
        args['car'] = car
        args['car_documents'] = car_documents
        return render(
            request,
            'Edit/edit_car.html',
            args
        )


### ROUTES ###

def registerRoute(request):
    args = basicArguments(request)
    user_cars = Car.objects.filter(user=request.user)
    campus = Campus.objects.filter(university=request.user.university)

    args['user_cars'] = user_cars
    args['campus_list'] = campus
    return render(request, 'Panel/Driver/Routes/new_route.html', args)
