from datetime import datetime, timedelta

from Core.Notifications.models import Notification
from Core.Routes.models import RouteDay

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

# TIME FORMAT
FMT = '%H:%M:%S'


def basicArguments(request):
    args = {}
    args['request'] = request
    if not request.user.is_anonymous():
        try:
            args['session_type'] = request.session['session_type']
        except KeyError:
            args['session_type'] = None
        args['user'] = request.user
    else:
        args['user'] = None
    return args


def setSessionType(request, type):
    if type == "passenger":
        request.session['session_type'] = 'passenger'
    else:
        request.session['session_type'] = 'driver'


def canRequestRoute(user, route):
    all_notifications = Notification.objects.filter(request_user=user.pk)
    days = RouteDay.objects.filter(route=route)

    if all_notifications.count() == 0:
        return True

    for notification in all_notifications:
        day_integer = datetime.now().weekday()

        if day_integer == MONDAY:
            for day in days:
                if day.day == "Lunes":
                    if validTimeDiference(route.start_time):
                        return True
                    else:
                        return False
        if day_integer == TUESDAY:
            for day in days:
                if day.day == "Martes":
                    if validTimeDiference(route.start_time):
                        return True
                    else:
                        return False
        if day_integer == WEDNESDAY:
            for day in days:
                if day.day == "Miercoles":
                    if validTimeDiference(route.start_time):
                        return True
                    else:
                        return False
        if day_integer == THURSDAY:
            for day in days:
                if day.day == "Jueves":
                    if validTimeDiference(route.start_time):
                        return True
                    else:
                        return False
        if day_integer == FRIDAY:
            for day in days:
                if day.day == "Viernes":
                    if validTimeDiference(route.start_time):
                        return True
                    else:
                        return False
        if day_integer == SATURDAY:
            for day in days:
                if day.day == "Sabado":
                    if validTimeDiference(route.start_time):
                        return True
                    else:
                        return False


def validTimeDiference(start_time):
    # Max diference between two routes times
    time = datetime.strptime('3:00:00', FMT)
    time_interval = timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)

    tdelta = datetime.strptime(datetime.now().time().strftime(FMT), FMT) - datetime.strptime(
        start_time.strftime(FMT), FMT)
    if tdelta < time_interval:
        print "Cant request route"
        return False
    else:
        print "Can request route"
        return True
