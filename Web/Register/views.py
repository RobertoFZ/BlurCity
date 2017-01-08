#!/usr/bin/python
# -*- coding: latin-1 -*-

from django.shortcuts import render

# Create your views here.
from Core.Account.models import User
from Core.Studies.models import University, Major
from Core.baseFunctions import basicArguments


def registerUserView(request):
    args = basicArguments(request)
    if request.method == "POST":
        print("post")
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']

        major = Major.objects.get(name=request.POST['major'])
        university = major.university

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
            new_user = User()
            new_user.email = email
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.university = university.pk
            new_user.major = major.pk
            new_user.set_password(password)
            new_user.save()

        return render(
            request,
            'Register/register_user.html',
            args
        )
    elif request.method == "GET":
        print("GET")

        universitys = University.objects.all()
        majors = Major.objects.all()

        args['universitys'] = universitys
        args['majors'] = majors

        return render(
            request,
            'Register/register_user.html',
            args
        )
