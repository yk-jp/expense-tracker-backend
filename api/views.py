from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import models

@api_view(['GET'])
def getData(request):
    person = {"name": "users"}
    return Response(person)

# @api_view(['POST'])
# def postData(request):

#     return Response()
