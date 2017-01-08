def basicArguments(request):
    args = {}
    args['social_log'] = ""

    if not request.user.is_anonymous():
        args['user'] = request.user
    else:
        args['user'] = None
    return args
