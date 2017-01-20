from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.template import RequestContext

from Core.baseFunctions import basicArguments, setSessionType
from Web.Panel.views import panelView


def choiceLoginTypeView(request):
    args = basicArguments(request)
    return render(
        request,
        'choice.html',
        args
    )


def loginView(request, type):
    args = basicArguments(request)

    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        setSessionType(request, type)
        return loginUser(request, email, password)
    else:
        logout(request)
        setSessionType(request, type)
        return render(request, 'login.html', args)


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
