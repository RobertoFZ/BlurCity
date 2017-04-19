# -*- coding: utf-8 -*-
import json

from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from django.core import serializers
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from BlurCity.settings import EMAIL_HOST_USER
from Core.Account.models import User
from Core.Cars.models import Car
from Core.Studies.models import University, Major, Campus
from Core.baseFunctions import basicArguments


def homePageView(request):
    return render(
        request,
        'Home/index.html'
    )


def howToJoinUs(request):
    args = basicArguments(request)
    if request.method == "GET":
        return render(
            request,
            'how_to_join_us.html',
            args
        )
    else:
        try:
            name = request.POST['name']
            email = request.POST['email']
            business = request.POST['business']
            tel = request.POST['tel']
            owner_name = request.POST['owner_name']
            country = request.POST['country']
            state = request.POST['state']
            city = request.POST['city']

            # SEND EMAIL FOR NOTIFY
            body = u'Nuevo contacto de Blur City \n\n' \
                   u'Nomre: %s \n' \
                   u'Correo electrónico: %s \n' \
                   u'Nombre de la institución o empresa: %s \n' \
                   u'Teléfono: %s \n' \
                   u'Nombre del representante legal: %s \n' \
                   u'País: %s \n' \
                   u'Estado: %s \n' \
                   u'Municipio: %s' % (name, email, business, tel, owner_name, country, state, city)
            email = EmailMessage(subject=u'Nuevo Contacto', body=body, to=[EMAIL_HOST_USER])
            email.send()
            return render(request, 'how_to_join_us.html', {'send': True})
        except:
            return render(request, 'how_to_join_us.html', {'error': True})


# ADMIN FUNCTIONS

def adminLogin(request):
    args = basicArguments(request)
    errors = []
    if request.user.is_anonymous():
        if request.POST:
            email = request.POST['email']
            password = request.POST['password']
            try:
                user = User.objects.get(email=email)
                if user.is_validated:
                    if user.user_admin_type == 0 or user.user_admin_type == 1 or user.user_admin_type == 2:
                        return loginUser(request, email, password)
                    else:
                        errors.append("El usuario no corresponde a un usuario administrativo de BlurCity")
                        args['errors'] = errors
                        return render(request, 'admin_login.html', args)
                else:
                    errors.append("El usuario administrativo no ha sido validado por BlurCity")
                    args['errors'] = errors
                    return render(request, 'admin_login.html', args)
            except User.DoesNotExist:
                errors.append("No existe un usuario con ese correo")
                args['errors'] = errors
                return render(request, 'admin_login.html', args)
        else:
            logout(request)
            return render(request, 'admin_login.html', args)
    else:
        if request.user.user_admin_type == 0 or request.user.user_admin_type == 1 or request.user.user_admin_type == 2:
            return redirect('/administration/admin_panel')
        else:
            errors.append("El usuario no corresponde a un usuario administrativo de BlurCity")
            args['errors'] = errors
            return render(request, 'admin_login.html', args)


def registerAdminUserView(request):
    if request.user.user_admin_type == 0:
        args = basicArguments(request)
        if request.method == "POST":
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password = request.POST['password']
            user_admin_type = request.POST['user_type']
            university_pk = request.POST['university']

            try:
                user = User.objects.get(email=email)
                errors = []
                errors.append(u"Ya existe un usuario con el correo electrónico ingresado")
                args['errors'] = errors
                args['email'] = email
                args['first_name'] = first_name
                args['last_name'] = last_name

                return render(
                    request,
                    'Admin/new_admin_user.html',
                    args
                )
            except User.DoesNotExist:
                args['created'] = True
                new_user = User()
                new_user.email = email
                new_user.first_name = first_name
                new_user.last_name = last_name
                new_user.university = university_pk
                new_user.set_password(password)
                new_user.user_admin_type = user_admin_type
                new_user.save()

            return render(
                request,
                'Admin/new_admin_user.html',
                args
            )
        elif request.method == "GET":
            args['universitys'] = University.objects.all()
            return render(
                request,
                'Admin/new_admin_user.html',
                args
            )
    else:
        return redirect('/administration/admin_panel')


def loginUser(request, username, password):
    log_user = authenticate(username=username, password=password)

    if log_user is not None:
        login(request, log_user)
        return redirect('/administration/admin_panel')
    else:
        return redirect('/administration')


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/administration')


def adminPanel(request):
    args = basicArguments(request)

    return render(request, 'Admin/panel.html', args)


def validUserList(request):
    args = basicArguments(request)
    user = request.user
    if not user.is_anonymous():
        if user.user_admin_type == 0 or user.user_admin_type == 2:
            users = User.objects.all().exclude(email=request.user.email)
            users_list = []
            admins_users_list = []

            if user.user_admin_type == 0:
                for user in users:
                    if user.user_admin_type == 3:
                        university_name = ""
                        major_name = ""
                        try:
                            university_name = University.objects.get(pk=user.university).name
                            major_name = Major.objects.get(pk=user.major)
                        except University.DoesNotExist, Major.DoesNotExist:
                            print "Error"

                        new_entry = {
                            'pk': user.pk,
                            'name': user.first_name + " " + user.last_name,
                            'email': user.email,
                            'university': university_name,
                            'major': major_name,
                            'date_joined': user.date_joined,
                            'is_validated': user.is_validated
                        }
                        users_list.append(new_entry)
                    else:
                        new_entry = {
                            'pk': user.pk,
                            'name': user.first_name + " " + user.last_name,
                            'email': user.email,
                            'type': user.user_admin_type,
                            'date_joined': user.date_joined,
                            'is_validated': user.is_validated
                        }
                        admins_users_list.append(new_entry)
            else:
                for user in users:
                    if user.university == request.user.university and user.user_admin_type != 1 and user.user_admin_type != 0:
                        university_name = ""
                        major_name = ""
                        try:
                            university_name = University.objects.get(pk=user.university).name
                            major_name = Major.objects.get(pk=user.major)
                        except (University.DoesNotExist, Major.DoesNotExist):
                            print "Error tipo 2"

                        new_entry = {
                            'pk': user.pk,
                            'name': user.first_name + " " + user.last_name,
                            'email': user.email,
                            'university': university_name,
                            'major': major_name,
                            'date_joined': user.date_joined,
                            'is_validated': user.is_validated
                        }
                        users_list.append(new_entry)

            args['users'] = users_list
            args['admin_users'] = admins_users_list
            return render(request, 'Admin/validated_users.html', args)
        else:
            return redirect('/')
    else:
        return redirect('/')


def validCarList(request):
    args = basicArguments(request)
    user = request.user
    if not user.is_anonymous():
        if user.user_admin_type == 0 or user.user_admin_type == 2:
            cars = Car.objects.all()
            car_list = []

            for car in cars:

                if user.user_admin_type == 2:
                    if car.user.university == request.user.university:
                        new_entry = {
                            'pk': car.pk,
                            'owner': car.user.first_name + " " + car.user.last_name,
                            'brand': car.brand,
                            'model': car.model,
                            'registration_tag': car.registration_tag,
                            'validated': car.validated
                        }
                        car_list.append(new_entry)
                else:
                    new_entry = {
                        'pk': car.pk,
                        'owner': car.user.first_name + " " + car.user.last_name,
                        'brand': car.brand,
                        'model': car.model,
                        'registration_tag': car.registration_tag,
                        'validated': car.validated
                    }
                    car_list.append(new_entry)

            args['cars'] = car_list
            return render(request, 'Admin/cars_list.html', args)
        else:
            return redirect('/administration')
    else:
        return redirect('/')


def universityList(request):
    args = basicArguments(request)
    user = request.user
    if not user.is_anonymous():
        if user.user_admin_type == 0:
            university = University.objects.all()

            args['universitys'] = university
            return render(request, 'Admin/university_list.html', args)
        else:
            return redirect('/administration')
    else:
        return redirect('/')


def campusList(request):
    args = basicArguments(request)
    user = request.user
    if not user.is_anonymous():
        if user.user_admin_type == 1:
            university = University.objects.get(pk=user.university)
            campus = Campus.objects.filter(university=university)

            args['campus'] = campus
            return render(request, 'Admin/campus_list.html', args)
        else:
            return redirect('/administration')
    else:
        return redirect('/')


def majorsList(request):
    args = basicArguments(request)
    user = request.user
    if not user.is_anonymous():
        if user.user_admin_type == 1:
            university = University.objects.get(pk=user.university)
            campus = Campus.objects.filter(university=university)
            majors = Major.objects.filter(campus__university=university)
            args['majors'] = majors
            args['campus'] = campus
            return render(request, 'Admin/majors_list.html', args)
        else:
            return redirect('/administration')
    else:
        return redirect('/')


def sendEmail(request):
    args = basicArguments(request)
    universitys = University.objects.all()

    args['universitys'] = universitys

    if request.method == "POST":
        university = University.objects.get(pk=request.POST['university'])
        campus = Campus.objects.get(pk=request.POST['campus'])
        message = request.POST['message']

        users = User.objects.filter(university=university.pk)
        users_to_send_message = []
        for user in users:
            major = Major.objects.get(pk=user.major)
            if major.campus == campus:
                users_to_send_message.append(user.email)

        # SEND EMAIL FOR NOTIFY
        email = EmailMultiAlternatives('Mensaje de BlurCity', message, to=users_to_send_message)
        email.send()
        args['message'] = "Mensaje enviado correctamente"
        return render(
            request,
            'Admin/send_email.html',
            args
        )
    else:
        return render(
            request,
            'Admin/send_email.html',
            args
        )


def contactFunction(request):
    try:
        name = request.POST['name']
        email = request.POST['email']
        business = request.POST['business']
        tel = request.POST['tel']
        owner_name = request.POST['owner_name']
        country = request.POST['country']
        state = request.POST['state']
        city = request.POST['city']

        # SEND EMAIL FOR NOTIFY
        body = u'Nuevo contacto de Blur City \n\n' \
               u'Nomre: %s \n' \
               u'Correo electrónico: %s \n' \
               u'Nombre de la institución o empresa: %s \n' \
               u'Teléfono: %s \n' \
               u'Nombre del representante legal: %s \n' \
               u'País: %s \n' \
               u'Estado: %s \n' \
               u'Municipio: %s' % (name, email, business, tel, owner_name, country, state, city)
        email = EmailMessage(subject=u'Nuevo Contacto', body=body, to=[EMAIL_HOST_USER])
        email.send()
        return render(request, 'how_to_join_us.html', {'send': True})
    except:
        return render(request, 'how_to_join_us.html', {'error': True})


# ADMIN WEBSERVICES
@csrf_exempt
def getMajorsFromUniversity(request):
    try:
        university = University.objects.get(pk=request.POST['university_pk'])
        majors = Major.objects.filter(campus__university=university)
        data = serializers.serialize('json', majors)
        return HttpResponse(data)
    except:
        return HttpResponse(0)


@csrf_exempt
def getCampusFromUniversity(request):
    try:
        university = University.objects.get(pk=request.POST['university_pk'])
        campus = Campus.objects.filter(university=university)
        data = serializers.serialize('json', campus)
        return HttpResponse(data)
    except:
        return HttpResponse(0)


@csrf_exempt
def deleteUser(request):
    try:
        User.objects.get(pk=request.POST['id']).delete()
        return HttpResponse(1)
    except:
        return HttpResponse(0)


@csrf_exempt
def changeValidateStatus(request):
    try:
        user_pk = request.POST['user_pk']
        user = User.objects.get(pk=user_pk)

        if user.is_validated:
            user.is_validated = False
        else:
            user.is_validated = True
        user.save()

        return HttpResponse("1")
    except:
        return HttpResponse("0")


@csrf_exempt
def changeCarValidateStatus(request):
    try:
        car_pk = request.POST['car_pk']
        car = Car.objects.get(pk=car_pk)
        print car
        if car.validated:
            car.validated = False
        else:
            car.validated = True
        car.save()

        return HttpResponse("1")
    except:
        return HttpResponse("0")


@csrf_exempt
def addUniversity(request):
    try:
        university_name = request.POST['university_name']
        university = University(name=university_name)
        university.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


@csrf_exempt
def addCampus(request):
    try:
        university_pk = request.POST['university_pk']
        campus_name = request.POST['campus_name']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        university = University.objects.get(pk=university_pk)

        campus = Campus(
            university=university,
            name=campus_name,
            latitude=latitude,
            longitude=longitude
        )
        campus.save()

        return HttpResponse("1")
    except:
        return HttpResponse("0")


@csrf_exempt
def addMajor(request):
    try:
        campus_pk = request.POST['campus_pk']
        major_name = request.POST['major_name']
        campus = Campus.objects.get(pk=campus_pk)

        major = Major(campus=campus, name=major_name)
        major.save()

        return HttpResponse("1")
    except:
        return HttpResponse("0")


@csrf_exempt
def deleteUniversity(request):
    try:
        university = University.objects.get(pk=request.POST['university_pk']).delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@csrf_exempt
def deleteCampus(request):
    try:
        campus = Campus.objects.get(pk=request.POST['campus_pk']).delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@csrf_exempt
def deleteMajor(request):
    try:
        major = Major.objects.get(pk=request.POST['major_pk']).delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")
