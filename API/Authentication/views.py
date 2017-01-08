import json

# Create your views here.
from rest_framework import status
from rest_framework.response import Response

from Core.Account.models import User


def register_user(request):
    print(request.body)
    body = json.loads(request.body)
    first_name = body['fields']['first_name']
    last_name = body['fields']['last_name']
    email = body['fields']['email']
    password = body['fields']['password']
    is_admin = body['fields']['is_admin']

    new_user = User()
    new_user.first_name = first_name
    new_user.last_name = last_name
    new_user.email = email
    new_user.set_password(password)
    new_user.is_admin = is_admin
    new_user.save()
    return Response(data=None, status=status.HTTP_200_OK)
