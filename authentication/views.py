from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from core.models import User
from core.serializers import UserSerializer
from django.core.exceptions import ValidationError
import simplejson as json


@api_view(['POST'])
def register_user(request):
  print("body: ", json.dumps(request.data, indent=4)) 
  
  new_account = {
    "email": "",
    "username" : "user",
    "password" : "",
    **request.data
  } 
  
  try:
    User.objects.create_user(new_account["email"],new_account["username"],new_account["password"])
    
  except (ValueError,ValidationError) as e:
    return Response(
      {   
          "message": e.args[0],
          "is_success":False
      },
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
      ) 
  
  except Exception as e:
    return Response(
      {   
          "message":"Failed to register account. Please try again",
          "is_success":False
      },
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
      ) 
    
  return Response(
      {
          "message": "successfully registered",
          "is_success": True
      })