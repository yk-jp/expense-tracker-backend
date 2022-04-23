from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from core.models import User, Category, Transaction
from core.serializers import UserSerializer 
import simplejson as json


@api_view(['GET'])
def register_user(request):
  print("body: ", json.dumps(request.data, indent=4))    
  
  user = User.objects.create_user('user@gmail.com', 'user', 'hays1228')
  
  u = User.objects.get(name='user')
  u = UserSerializer(
            u).data
  print("body: ", u) 
   
  return Response(
    {
      "password"
    } ,status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)