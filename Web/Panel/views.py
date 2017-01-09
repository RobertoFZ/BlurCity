from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext

from Core.Cars.models import Car, CarDocument
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
