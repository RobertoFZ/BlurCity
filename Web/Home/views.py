from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from Core.Account.models import User
from Core.Studies.models import University, Major, Campus
from Core.baseFunctions import basicArguments


def homePageView(request):
    return render(
        request,
        'Home/index.html'
    )


# ADMIN FUNCTIONS

def validUserList(request):
    args = basicArguments(request)

    if not request.user.is_anonymous():
        if request.user.is_admin:
            users = User.objects.all().exclude(email=request.user.email)
            users_list = []

            for user in users:
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

            universitys = University.objects.all()
            campus = Campus.objects.all()
            majors = Major.objects.all()

            args['users'] = users_list
            args['universitys'] = universitys
            args['majors'] = majors
            args['campus'] = campus
            return render(request, 'Admin/validated_users.html', args)
        else:
            return redirect('/')
    else:
        return redirect('/')


# ADMIN WEBSERVICES
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