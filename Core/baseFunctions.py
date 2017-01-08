def basicArguments(request):
    args = {}
    args['request'] = request
    if not request.user.is_anonymous():
        args['user'] = request.user
    else:
        args['user'] = None
    return args


def setSessionType(request, type):
    if type == "passenger":
        request.session['session_type'] = 'passenger'
    else:
        request.session['session_type'] = 'driver'
