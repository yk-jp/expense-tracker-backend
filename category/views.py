from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import User
from core.serializers import CategorySerializer
from django.core.exceptions import ValidationError
import simplejson as json

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_category_all(request, type):
  user = request.user
  
  try:
    category_all = user.category_set.filter(category_type=type)
    category_all = CategorySerializer(category_all, many=True).data
  
  except Exception as e:
    return Response(
      {   
          "message":"Failed to fetch data. Please try again",
          "is_success":False
      },
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
      ) 
    
  return Response(
      {
          "result": {
            "category_all": category_all
          },
          "message": "successfully fetched",
          "is_success": True
      })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_category(request):
  print("body: ", json.dumps(request.data, indent=4)) 
  
  user = request.user
  
  new_record = {
    **request.data,
    "user": user.id
  } 
  
  try:
    new_category = CategorySerializer(data = new_record) 
    
    if new_category.is_valid() and new_category.create_validation():
      user.category_set.create(**new_record)
       
    else:
        return Response(
            {
            "message": {
                **new_category.errors
            },
            "is_success" : False
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
  
  except (ValueError,ValidationError) as e:
    raise e
    return Response(
      {   
          "message": e.args[0],
          "is_success":False
      },
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
      ) 

  except Exception as e:
    raise e
    return Response(
      {   
          "message":"Failed to register new category. Please try again",
          "is_success":False
      },
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
      ) 
    
  return Response(
      {
          "message": "successfully registered",
          "is_success": True
      })
 
 
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_category(request, id):
  print("body: ", json.dumps(request.data, indent=4)) 
  
  user = request.user 
  
  new_record = {
      **request.data,
      "user": user.id
  }
   
  try:
    new_category = CategorySerializer(data = new_record) 
    
    if new_category.is_valid() and new_category.update_validation(id):
      user.category_set.filter(pk=id).update(**new_record)
       
    else:
        return Response(
            {
            "message": {
                **new_category.errors
            },
            "is_success" : False
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
  
  except (ValueError,ValidationError) as e:
    raise e
    return Response(
      {   
          "message": e.args[0],
          "is_success":False
      },
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
      ) 

  except Exception as e:
    raise e
    return Response(
      {   
          "message":"Failed to update category. Please try again",
          "is_success":False
      },
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
      ) 
    
  return Response(
      {
          "message": "successfully updated",
          "is_success": True
      })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_category(request, id):
  user = request.user 
  
  try:
    user.category_set.filter(pk=id).delete()
  
  except Exception as e:
    return Response(
      {   
          "message":'Failed to delete data. Please try again',
          "is_success":False
      },
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
      ) 
    
  return Response(
      {
          "message": "successfully deleted",
          "is_success": True
      })
  