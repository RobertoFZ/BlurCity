from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


# Create your views here.
from Core.baseFunctions import basicArguments


def choiceLoginTypeView(request):
    args = basicArguments(request)
    return render(
        request,
        'choice.html',
        args
    )

def loginView(request):
    args = basicArguments(request)
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        return loginUser(request, email, password)
    else:
        logout(request)
        return render(request, 'login.html')


def loginUser(request, username, password):
    log_user = authenticate(username=username, password=password)

    if log_user is not None:
        login(request, log_user)
        return HttpResponseRedirect('/')
    else:
        return redirect('/authentication/login')


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/authentication/login')
