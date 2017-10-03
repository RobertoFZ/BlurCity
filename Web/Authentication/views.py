# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.template import RequestContext
from django.views import View

from Core.Account.models import User
from Core.baseFunctions import basicArguments, setSessionType
from Web.Panel.views import panelView


def choiceLoginTypeView(request):
    args = basicArguments(request)
    logoutUser(request)
    return render(
        request,
        'choice_login.html',
        args
    )


def loginView(request, type):
    args = basicArguments(request)

    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        setSessionType(request, type)
        try:
            user = User.objects.get(email=email)
            if user.is_validated:
                return loginUser(request, email, password)
            else:
                errors = []
                errors.append("Usuario no validado por la institucion")
                args['errors'] = errors
                return render(request, 'login_user.html', args)
        except User.DoesNotExist:
            errors = []
            errors.append("No existe un usuario con ese correo")
            args['errors'] = errors
            return render(request, 'login_user.html', args)
    else:
        logout(request)
        setSessionType(request, type)
        return render(request, 'login_user.html', args)


def loginUser(request, username, password):
    log_user = authenticate(username=username, password=password)

    if log_user is not None:
        login(request, log_user)
        return redirect('/panel/')
    else:
        return redirect('/authentication/choice_login_type')


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/authentication/choice_login_type')


class EditProfileView(View):
    template_name = "Edit/edit_profile.html"

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request):
        edit_type = request.POST['edit_type']

        if edit_type == "password":
            current_pasword = request.POST['current_password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']

            if new_password != confirm_password:
                errors = [u"Las contraseñas no coinciden"]
                context = {
                    'errors': errors
                }
                return render(request, self.template_name, context)
            else:
                request.user.set_password(new_password)
                request.user.save()
                is_edited = True
                context = {
                    'edited': is_edited
                }
                return render(request, self.template_name, context)
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']

            try:
                image = request.FILES['image']
            except:
                image = None

            try:
                user = User.objects.get(email=email)
                if user == request.user:
                    user = None
            except User.DoesNotExist:
                user = None
            if user:
                errors = [u"El correo electrónico proporcionado ya esta en uso"]
                context = {
                    'errors': errors
                }
                return render(request, self.template_name, context)
            else:
                user = request.user
                user.first_name = first_name
                user.last_name = last_name
                user.email = email

                if image:
                    if user.image_profile:
                        user.image_profile.delete()
                        user.image_profile = image
                    else:
                        user.image_profile = image

                user.save()
                is_edited = True
                context = {
                    'edited': is_edited
                }
                return render(request, self.template_name, context)
